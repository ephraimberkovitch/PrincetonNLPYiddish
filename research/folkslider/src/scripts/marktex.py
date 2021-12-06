import mistune 
import warnings

class LyricsRenderer(mistune.Renderer):
    # Unsupported Elements
    def __init__(self, *args, **kwargs):
      super().__init__(hard_wrap=True, *args, **kwargs)
    
    def not_supported(self, string):
        warnings.warn('%s is not supported, \
output may be broken.' % \
            (stack()[1][3]), Warning, stacklevel=4)
        return self.text(string)

    def block_code(self, string, *_):
        return self.not_supported(string)
    def block_quote(self, string, *_):
        return self.not_supported(string)
    def block_html(self, string, *_):
        return self.not_supported(string)
    def header(self, string, *_):
        return self.not_supported(string)
    def hrule(self, *_):
        return self.not_supported('')
    def list(self, string, *_):
        return self.not_supported(string)
    def list_item(self, string, *_):
        return self.not_supported(string)
    def table(self, string, *_):
        return self.not_supported(string)
    def table_row(self, string, *_):
        return self.not_supported(string)
    def table_cell(self, string, *_):
        return self.not_supported(string)
    def autolink(self, string, *_):
        return self.not_supported(string)
    def codespan(self, string, *_):
        return self.not_supported(string)
    def image(self, string, *_):
        return self.not_supported(string)
    def link(self, string, *_):
        return self.not_supported(string)
    def strikethrough(self, string, *_):
        return self.not_supported(string)
    def inline_html(self, string, *_):
        return self.not_supported(string)
    # Verse Elements
    
    def paragraph(self, text):
        return('%s\\\\!\n\n' % text)
    def emphasis(self, text):
        return('{\em %s}' % text)
    def double_emphasis(self, text):\
        return self.emphasis(text)
    def linebreak(self):
        return('\\\\*\n')
    def newline(self):
        return('\\\\*\n')
