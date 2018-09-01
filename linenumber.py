from tkinter import * 
from tkinter import Canvas, Text, Frame

class LineNumber(Canvas):
    def __init__(self,*args,**kwargs):
        Canvas.__init__(self,*args,**kwargs)

    def attach(self, text):
        self.text = text

    def set_linenumber(self, *args):
        """Set Line Number"""
        self.delete("all")

        i = self.text.index("@0,0")  
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y, anchor="nw", text=linenum) 
            i = self.text.index("%s+1line" % i)   

class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        if (args[0] in ("insert","replace","delete") or
            args[0:3] == ("mark","set","insert") or
            args[0:2] == ("xview","moveto") or
            args[0:2] == ("xview","scroll") or
            args[0:2] == ("yview","moveto") or
            args[0:2] == ("yview","scroll")):
            self.event_generate("<<Change>>", when="tail")

        return result
                