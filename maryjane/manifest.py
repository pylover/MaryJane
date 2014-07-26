# -*- coding: utf-8 -*-
import yaml
import time
import os.path
from watchdog.observers import Observer
from maryjane.tags import TaskTag, SubprocessActionTag, TemplateTag, ObservableTaskTag, EvaluateTag, OptionsTag
from maryjane.helpers import get_source_dirs, has_file_overlap, split_paths
from watchdog.events import FileSystemEventHandler

__author__ = 'vahid'


class ManifestFileEventHandler(FileSystemEventHandler):
    def __init__(self, manifest):
        self.manifest = manifest
        super(FileSystemEventHandler, self).__init__()

    def on_any_event(self, event):
        paths = []
        if hasattr(event, 'src_path'):
            paths += split_paths(event.src_path)
        if hasattr(event, 'dest_path'):
            paths += split_paths(event.dest_path)

        if has_file_overlap(paths, self.manifest.filename):
            self.manifest.reload_file()
            self.manifest.execute()


class Manifest(object):

    def __init__(self, filename, working_dir='.'):
        self.filename = filename
        self.working_dir = working_dir
        self.configure_yaml()
        self.tasks = {}
        self.watching_tasks = {}
        self._context = {}
        self.reload_file()

    def reload_file(self):
        manifest_dir = os.path.dirname(self.filename)
        self._context = dict(manifest_dir= '.' if not manifest_dir else manifest_dir,
                             working_dir=self.working_dir)
        with open(self.filename) as manifest_file:
            config = yaml.load(manifest_file)
        self.tasks = {k: v for k, v in config.iteritems() if isinstance(v, TaskTag)}
        self.watching_tasks = {k: v for k, v in config.iteritems() if isinstance(v, ObservableTaskTag)}
        if 'context' in config and isinstance(config['context'], OptionsTag):
            self._context.update(config['context'].to_dict())
            self._context.update(self.tasks)

    def __getattr__(self, name):
        if name in self.tasks:
            return self.tasks[name]
        raise AttributeError

    @property
    def context(self):
        return self._context

    def execute(self):
        for task_name, task in self.tasks.iteritems():
            task.execute_actions()

    def configure_yaml(self):
        def specialize(func):
            def _decorator(*args, **kwargs):
                return func(self, *args, **kwargs)
            return _decorator
        yaml.add_constructor('!options', specialize(OptionsTag.from_yaml_node))
        yaml.add_constructor('!subprocess', specialize(SubprocessActionTag.from_yaml_node))
        yaml.add_constructor('!task', specialize(TaskTag.from_yaml_node))
        yaml.add_constructor('!watch', specialize(ObservableTaskTag.from_yaml_node))
        yaml.add_constructor('!template', specialize(TemplateTag.from_yaml_node))
        yaml.add_constructor('!eval', specialize(EvaluateTag.from_yaml_node))

    def watch(self, block=False):
        observer = Observer()

        # Add watch for manifest file
        observer.schedule(ManifestFileEventHandler(self),
                          get_source_dirs(self.filename)[0])


        for task_name, task in self.watching_tasks.iteritems():
            for directory in get_source_dirs(task.watch):
                observer.schedule(task.create_event_handler(), directory)

        observer.start()
        if block:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

if __name__ == '__main__':
    fn = 'tests/maryjane.yaml'
    m = Manifest(fn, working_dir='tests')

    m.execute()
    m.watch(block=True)

