import sublime, sublime_plugin, re

class OpenSearchInNewTab(sublime_plugin.EventListener):
    cache = {}

    def on_new_async(self, view):
        if view.element() == 'find_in_files:output':
            while view.size() == 0:
                pass

            first_line_region = view.line(sublime.Region(0, 0))
            first_line = view.substr(first_line_region)
            match = re.search('"(.*?)("(?: \(.*\))?)?$', first_line)

            if match:
                query = match.group(1).rstrip()

                if not match.group(2):
                    query += '↲'

                if len(query) > 16:
                    query = query[:16].rstrip() + '…'

                key = hash(query)
                self.cache[key] = self.cache.get(key, 0) + 1

                if self.cache[key] > 1:
                    query += ' (' + str(self.cache[key]) + ')'

                view.set_name(view.name() + ': ' + query)
