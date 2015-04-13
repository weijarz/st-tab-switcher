import sublime
import sublime_plugin
import os


class TabSwitcherCommand(sublime_plugin.WindowCommand):

    def run(self):
        items = self.__get_items()
        self.window.show_quick_panel(items, self.__select, 0)

    def __get_views(self):
        views = list(self.window.views())

        for view in views:
            if view.id() == self.window.active_view().id():
                views.remove(view)
                break

        for vid in recent_view_ids[:]:
            for view in views:
                if view.id() == vid:
                    views.remove(view)
                    views.insert(0, view)
                    break
            else:
                recent_view_ids.remove(vid)

        return views

    def __get_items(self):
        self.__item_view_ids = []
        items = []
        for view in self.__get_views():
            items.append([self.__get_display_name(view), view.file_name() or ''])
            self.__item_view_ids.append(view.id())
        return items

    def __select(self, index):
        if index != -1:
            for view in self.window.views():
                if view.id() == self.__item_view_ids[index]:
                    self.window.focus_view(view)
                    break

    def __get_display_name(self, view):
        mod_star = '*' if view.is_dirty() else ''

        if view.is_scratch() or not view.file_name():
            disp_name = view.name() or 'untitled'
        else:
            disp_name = os.path.basename(view.file_name())

        return '%s%s' % (disp_name, mod_star)

recent_view_ids = []
class Listener(sublime_plugin.EventListener):

    def on_deactivated(self, view):
        if view.id() in recent_view_ids:
            recent_view_ids.remove(view.id())
        recent_view_ids.append(view.id())
