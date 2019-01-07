"""Note Editor Software. Simple text editor created with tkinter module
Developed by : Karan Chaudhari
"""

from tkinter import *
from tkinter import TclError, StringVar
from PIL import Image, ImageTk
from tkinter.font import Font
from tkinter import messagebox, filedialog, simpledialog
from idlelib.searchbase import SearchDialogBase
from idlelib import searchengine
from idlelib import search
from linenumber import LineNumber, CustomText
import tkinter.colorchooser
import os, time

class Note_Editor:
    """Create Main class of Note Editor"""
    from idlelib.statusbar import MultiStatusBar
    fontsize = 12 # set default fontsize
    font = "Consolas" # set default font
    fontstyle = "normal" # set default fontstyle
    def __init__(self, root):
        self.root = root
        self.title = "Note Editor"
        self.file_path = None
        self.set_title()

        root.protocol("WM_DELETE_WINDOW", self.exit) 

        # *************************    Create Main Menu   ********************************
        self.mainmenu = Menu(root)
        filemenu = Menu(self.mainmenu, tearoff=0)
        # ************************    Create File Menu    ********************************
        self.mainmenu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label="New File", accelerator='Ctrl+N', command=self.new)
        filemenu.add_command(label="Open File", accelerator='Ctrl+O', command=self.open)
        filemenu.add_separator()
        filemenu.add_command(label='Save', accelerator='Ctrl+S', command=self.save)
        filemenu.add_command(label='Save As', accelerator='Ctrl+Shift+S', command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', accelerator='Alt+F4', command=self.exit)
        # ************************   Create Edit Menu    **********************************
        editmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label="Undo", accelerator='Ctrl+Z', command=self.undo)
        editmenu.add_command(label="Redo", accelerator='Ctrl+Y', command=self.redo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", accelerator='Ctrl+X', command=self.cut)
        editmenu.add_command(label="Copy", accelerator='Ctrl+C', command=self.copy)
        editmenu.add_command(label="Paste", accelerator='Ctrl+V', command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="Go To Line", accelerator='Ctrl+G', command=self.go_to)
        editmenu.add_command(label="Find", accelerator='Ctrl+F', command=self.show_find)
        editmenu.add_command(label="Replace", accelerator='Ctrl+H', command=self.show_replace)
        editmenu.add_separator()
        editmenu.add_command(label="Select All", accelerator='Ctrl+A', command=self.select_all)
        editmenu.add_command(label="Delete", accelerator='Del', command=self.delete)
        editmenu.add_command(label="Date/Time", accelerator='F5', command=self.date_time)
        # ************************   Create Font Menu   *************************************
        fontmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Font", menu=fontmenu)
        fontmenu.add_cascade(label="Font", command=self.font_change)
        fontmenu.add_command(label="Font Size", command=self.font_size)
        fontmenu.add_command(label="Font Color", command=self.font_color)
        fontmenu.add_separator()
        fontmenu.add_command(label="Bold", accelerator='Ctrl+B', command=self.bold)
        fontmenu.add_command(label="Italic", accelerator='Ctrl+I', command=self.italic)
        fontmenu.add_command(label="Underline", accelerator='Ctrl+U', command=self.underline)
        fontmenu.add_command(label="Overstrike", accelerator='Ctrl+T', command=self.overstrike)
        # ************************    Create About Menu   *************************************
        aboutmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="About", menu=aboutmenu)
        aboutmenu.add_command(label="About Note Editor", command=self.about) 

        # ************************   Create Toolbar Menu   ***********************************
        self.toolbar = Frame(root, relief=FLAT)
    
        self.imgn = Image.open("icons/new.png")
        eimgn = ImageTk.PhotoImage(self.imgn)
        newButton = Button(self.toolbar, image=eimgn, relief=FLAT, command=self.new)
        newButton.image = eimgn
        newButton.pack(side=LEFT)

        self.imgo = Image.open("icons/open.png")
        eimgo = ImageTk.PhotoImage(self.imgo)
        openButton = Button(self.toolbar, image=eimgo, relief=FLAT, command=self.open)
        openButton.image = eimgo
        openButton.pack(side=LEFT)

        self.imgs = Image.open("icons/save.png")
        eimgs = ImageTk.PhotoImage(self.imgs)
        saveButton = Button(self.toolbar, image=eimgs, relief=FLAT, command=self.save)
        saveButton.image = eimgs
        saveButton.pack(side=LEFT)

        self.imgsa = Image.open("icons/save-as.png")
        eimgsa = ImageTk.PhotoImage(self.imgsa)
        saveasButton = Button(self.toolbar, image=eimgsa, relief=FLAT, command=self.save_as)
        saveasButton.image = eimgsa
        saveasButton.pack(side=LEFT)

        self.imgu = Image.open("icons/undo.png")
        eimgu = ImageTk.PhotoImage(self.imgu)
        undoButton = Button(self.toolbar, image=eimgu, relief=FLAT, command=self.undo)
        undoButton.image = eimgu
        undoButton.pack(side=LEFT)

        self.imgr = Image.open("icons/redo.png")
        eimgr = ImageTk.PhotoImage(self.imgr)
        redoButton = Button(self.toolbar, image=eimgr, relief=FLAT, command=self.redo)
        redoButton.image = eimgr
        redoButton.pack(side=LEFT)

        self.imgc = Image.open("icons/cut.png")
        eimgc = ImageTk.PhotoImage(self.imgc)
        cutButton = Button(self.toolbar, image=eimgc, relief=FLAT, command=self.cut)
        cutButton.image = eimgc
        cutButton.pack(side=LEFT)

        self.imgco = Image.open("icons/copy.png")
        eimgco = ImageTk.PhotoImage(self.imgco)
        copyButton = Button(self.toolbar, image=eimgco, relief=FLAT, command=self.copy)
        copyButton.image = eimgco
        copyButton.pack(side=LEFT)

        self.imgp = Image.open("icons/paste.png")
        eimgp = ImageTk.PhotoImage(self.imgp)
        pasteButton = Button(self.toolbar, image=eimgp, relief=FLAT, command=self.paste)
        pasteButton.image = eimgp
        pasteButton.pack(side=LEFT)

        self.imgf = Image.open("icons/find.png")
        eimgf = ImageTk.PhotoImage(self.imgf)
        findButton = Button(self.toolbar, image=eimgf, relief=FLAT, command=self.show_find)
        findButton.image = eimgf
        findButton.pack(side=LEFT)

        self.imgr = Image.open("icons/replace.png")
        eimgr = ImageTk.PhotoImage(self.imgr)
        replaceButton = Button(self.toolbar, image=eimgr, relief=FLAT, command=self.show_replace)
        replaceButton.image = eimgr
        replaceButton.pack(side=LEFT)

        self.imgse = Image.open("icons/select-all.png")
        eimgse = ImageTk.PhotoImage(self.imgse)
        selallButton = Button(self.toolbar, image=eimgse, relief=FLAT, command=self.select_all)
        selallButton.image = eimgse
        selallButton.pack(side=LEFT)

        self.imgd = Image.open("icons/delete.png")
        eimgd = ImageTk.PhotoImage(self.imgd)
        delButton = Button(self.toolbar, image=eimgd, relief=FLAT, command=self.delete)
        delButton.image = eimgd
        delButton.pack(side=LEFT)

        self.imgb = Image.open("icons/bold.png")
        eimgb = ImageTk.PhotoImage(self.imgb)
        boldButton = Button(self.toolbar, image=eimgb, relief=FLAT, command=self.bold)
        boldButton.image = eimgb
        boldButton.pack(side=LEFT)
        
        self.imgi = Image.open("icons/italic.png")
        eimgi = ImageTk.PhotoImage(self.imgi)
        italicButton = Button(self.toolbar, image=eimgi, relief=FLAT, command=self.italic)
        italicButton.image = eimgi
        italicButton.pack(side=LEFT)

        self.imgu = Image.open("icons/underline.png")
        eimgu = ImageTk.PhotoImage(self.imgu)
        underButton = Button(self.toolbar, image=eimgu, relief=FLAT, command=self.underline)
        underButton.image = eimgu
        underButton.pack(side=LEFT)

        self.imgf = Image.open("icons/fonts.png")
        eimgf = ImageTk.PhotoImage(self.imgf)
        fontsButton = Button(self.toolbar, image=eimgf, relief=FLAT, command=self.font_change)
        fontsButton.image = eimgf
        fontsButton.pack(side=LEFT)

        self.imgfs = Image.open("icons/font-size.png")
        eimgfs = ImageTk.PhotoImage(self.imgfs)
        fontsizeButton = Button(self.toolbar, image=eimgfs, relief=FLAT, command=self.font_size)
        fontsizeButton.image = eimgfs
        fontsizeButton.pack(side=LEFT)

        self.imgfc = Image.open("icons/font-color.png")
        eimgfc = ImageTk.PhotoImage(self.imgfc)
        fontcolorButton = Button(self.toolbar, image=eimgfc, relief=FLAT, command=self.font_color)
        fontcolorButton.image = eimgfc
        fontcolorButton.pack(side=LEFT)

        self.imga = Image.open("icons/about.png")
        eimga = ImageTk.PhotoImage(self.imga)
        aboutButton = Button(self.toolbar, image=eimga, relief=FLAT, command=self.about)
        aboutButton.image = eimga
        aboutButton.pack(side=LEFT)
        
        self.imge = Image.open("icons/exit.png")
        eimge = ImageTk.PhotoImage(self.imge)
        exitButton = Button(self.toolbar, image=eimge, relief=FLAT, command=self.exit)
        exitButton.image = eimge
        exitButton.pack(side=LEFT)

        self.toolbar.pack(side=TOP, fill=X)
        root.config(menu=self.mainmenu)
        # ***********************   Create Window Frame   ******************************
        frame = Frame(root)
        self.scrollbar = Scrollbar(frame, orient=VERTICAL)
        self.text = CustomText(frame, yscrollcommand=self.scrollbar.set, inactiveselectbackground='grey') # inactiveselectbackground is used for find and replace function
        self.linenumber = LineNumber(frame, width=30)
        self.linenumber.attach(self.text)
        self.linenumber.pack(side=LEFT, fill=Y)
        self.text.pack(fill=BOTH, side=LEFT, expand=1)
        self.scrollbar.pack(fill=Y,side=RIGHT)
        self.scrollbar.config(command=self.text.yview)
        self.status()
        frame.pack(fill=BOTH, side=LEFT, expand=1)

        # Bind text with _on_update function
        self.text.bind("<<Change>>", self._on_update)
        self.text.bind("<<Configure>>", self._on_update)

        self.fontvar = StringVar()
        self.fontvar.set(self.font)

        self.text.config(font=(self.font, self.fontsize, self.fontstyle))

    def _on_update(self, *args):
        """Update line number"""
        self.linenumber.set_linenumber()

    def save_if_modified(self, event=None, *args):
        """This function for any modified in file or document"""
        if self.text.edit_modified():
            responce = messagebox.askyesnocancel("Save?","This document has been modified. Do you want to save changes?")
            if responce:
                result = self.save()
                if result=='saved':
                    return True
                else:
                    return False
            else:
                return responce
        else:
            return True            

    def set_title(self, *args):
        """Set File title"""
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.title)        

    def new(self, event=None, *args):
        """Open New File"""
        result = self.save_if_modified()
        if result != None:
            self.text.delete("1.0","end")
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.file_path = None
            self.set_title()

    def open(self, event=None, filepath=None, *args):
        """Open Any saved file"""
        result = self.save_if_modified()
        if result != None:
            if filepath == None:
                filepath = filedialog.askopenfilename()
            if filepath != None and filepath != "":
                with open(filepath, encoding='ANSI') as f:
                    filecontent = f.read()
                self.text.delete("1.0","end")
                self.text.insert("1.0",filecontent)    
                self.text.edit_modified(False)
                self.file_path = filepath
                self.set_title()    

    def save(self, event=None, *args):
        """Save new file"""
        if self.file_path == None:
            result = self.save_as()
        else:
            result = self.save_as(filepath=self.file_path)
        return result

    def save_as(self, event=None, filepath=None, *args):
        """Save any changes in save file"""
        if filepath == None:
            filepath = filedialog.asksaveasfilename(filetype=(("Text File","*.txt"),("All Files","*.*")))
        try:
            with open(filepath, 'wb') as f:
                text = self.text.get("1.0","end")
                f.write(bytes(text,"UTF-8"))
                self.text.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return "saved"
        except FileNotFoundError:
            print('FileNotFoundError') 
            return "cancelled"       

    def exit(self, event=None, *args):
        """Before exit asking if any modification in file"""
        result = self.save_if_modified
        if result == None:
            self.root.destroy()
        if result != None:
            self.save_if_modified()
            self.root.destroy()    

    def undo(self, event=None, *args):
        """Undo Function"""
        try:
            self.text.event_generate('<<Undo>>')  
        except TclError:
            pass    

    def redo(self, event=None, *args):
        """Redo Function"""
        try:
            self.text.event_generate('<<Redo>>')
        except TclError:
            pass    

    def cut(self, event=None, *args):
        """Cut Function"""
        try:
            self.copy()
            self.text.delete("sel.first","sel.last")  
        except TclError:
            pass

    def copy(self, event=None, *args):
        """Copy Function"""
        try:
            self.text.clipboard_clear()
            text = self.text.get("sel.first","sel.last")
            self.text.clipboard_append(text)        
        except TclError:
            pass

    def paste(self, event=None, *args):
        """Paste Function"""
        try:
            text = self.text.clipboard_get()
            self.text.insert('insert',text)
        except TclError:
            pass    
 
    def go_to(self, event=None, *args):
        """Go to any line"""
        text = self.text
        lineno = simpledialog.askinteger("Go To","Go to line number", parent=text)
        if lineno is None:
            return "break"
        if lineno <= 0:
            text.bell()
            return "break"
        text.mark_set("insert","%d.0" % lineno) 
        text.see("insert")   
        return "break"    

    def show_find(self, event=None, *args):
        """Find Function"""
        self.text.tag_add("sel","1.0","end")
        setup(self.text).open(self.text)
        self.text.tag_remove("sel","1.0","end")

    def show_replace(self, event=None, *args):
        """Replace Function"""
        self.text.tag_add("sel","1.0","end")
        replace(self.text)
        self.text.tag_remove("sel","1.0","end")

    def select_all(self, event=None, *args):
        """Select All text"""
        self.text.tag_add('sel','1.0','end')

    def delete(self, event=None, *args):
        """Delete Function"""
        try:
            self.text.delete("sel.first","sel.last")
        except TclError:
            pass
  
    def date_time(self, event=None, *args):
        """Show Date & Time"""
        date_time = time.strftime("%d %b %Y , %r", time.localtime())
        self.text.insert("insert", date_time)
    
    def font_color(self, event=None, *args):
        """Change Font color"""
        try:
            (rgb, hx) = tkinter.colorchooser.askcolor()
            self.text.tag_add("color","sel.first","sel.last")
            self.text.tag_configure("color", foreground=hx)
        except TclError:
            pass

    def bold(self, event=None, *args):
        """Change Font in Bold or Bold to normal"""
        try:
            current_tag = self.text.tag_names("sel.first")
            if "bold" in current_tag:
                self.text.tag_remove("bold","sel.first","sel.last")
            else:
                self.text.tag_add("bold","sel.first","sel.last")
                bold_tag = Font(self.text, self.text.cget("font"))
                bold_tag.configure(weight="bold")
                self.text.tag_configure("bold",font=bold_tag) 
        except TclError:
            pass
                    
    def italic(self, event=None, *args):
        """Change Font in Italic or Italic to normal"""
        try:
            current_tag = self.text.tag_names("sel.first")
            if "italic" in current_tag:
                self.text.tag_remove("italic","sel.first","sel.last")
            else:
                self.text.tag_add("italic","sel.first","sel.last")
                italic_tag = Font(self.text, self.text.cget("font"))
                italic_tag.configure(slant="italic")
                self.text.tag_configure("italic", font=italic_tag)
        except TclError:
            pass     

    def underline(self, event=None, *args):
        """Set Underline in Font or remove Underline in Font"""
        try:
            current_tag = self.text.tag_names("sel.first")
            if "underline" in current_tag:
                self.text.tag_remove("underline","sel.first","sel.last")
            else:
                self.text.tag_add("underline","sel.first","sel.last")
                underline_font = Font(self.text, self.text.cget("font"))
                underline_font.configure(underline=1)
                self.text.tag_configure("underline", font=underline_font)    
        except TclError:
            pass

    def overstrike(self, event=None, *args):
        """Set Overstrike in Font or remove Overstrike in Font"""
        try:
            current_tag = self.text.tag_names("sel.first")
            if "overstrike" in current_tag:
                self.text.tag_remove("overstrike","sel.first","sel.last")
            else:
                self.text.tag_add("overstrike","sel.first","sel.last")
                overstrike_font = Font(self.text, self.text.cget("font")) 
                overstrike_font.configure(overstrike=1)
                self.text.tag_configure("overstrike", font=overstrike_font)   
        except TclError:
            pass

    def about(self, *args):
        """Show information of Note Editor"""
        messagebox.showinfo("About Note Editor","Develop By : Karan Chaudhari \nVersion : 1.0")
 
    def status(self, event=None, *args):
        """Create Statusbar"""
        self.statusbar = self.MultiStatusBar(self.root)
        self.statusbar.set_label('Statusbar','Statusbar',side=LEFT)
        self.statusbar.set_label('column','Col: ?', side=RIGHT, width=35)
        self.statusbar.set_label('line','Ln: ?', side=RIGHT)
        self.statusbar.pack(side=BOTTOM, fill=X)
        self.text.bind("<<set-line-and-column>>", self.set_line_and_column)
        self.text.event_add("<<set-line-and-column>>","<KeyRelease>","<ButtonRelease>")
        self.text.after_idle(self.set_line_and_column)
        
    def set_line_and_column(self, event=None, *args):
        """Set Line & Column for Statusbar"""
        line, column = self.text.index(INSERT).split('.')
        self.statusbar.set_label('column','Col: %s' % column)
        self.statusbar.set_label('line','Ln: %s' % line)

    def font_change(self):
        """Change Font"""
        Font_Change(self)

    def font_size(self):
        """Change Font Size"""
        Font_Size(self)

    def shortcut_keys(self, event=None, *args):
        """Set Shortcut keys for all function"""
        self.text.bind('<Control-N>', self.new)
        self.text.bind('<Control-n>', self.new)
        self.text.bind('<Control-O>', self.open)
        self.text.bind('<Control-o>', self.open)
        self.text.bind('<Control-S>', self.save)
        self.text.bind('<Control-s>', self.save)
        self.text.bind('<Control-Shift-S>', self.save_as)
        self.text.bind('<Control-Shift-s>', self.save_as)
        self.text.bind('<Control-G>', self.go_to)
        self.text.bind('<Control-g>', self.go_to)
        self.text.bind('<Control-F>', self.show_find)
        self.text.bind('<Control-f>', self.show_find)
        self.text.bind('<Control-H>', self.show_replace)
        self.text.bind('<Control-h>', self.show_replace)
        self.text.bind('<Control-A>',  self.select_all)
        self.text.bind('<Control-a>', self.select_all)
        self.text.bind('<Delete>', self.delete)
        self.text.bind('<F5>', self.date_time)
        self.text.bind('<Control-B>', self.bold)
        self.text.bind('<Control-b>', self.bold)
        self.text.bind('<Control-I>', self.italic)
        self.text.bind('<Control-i>', self.italic)
        self.text.bind('<Control-U>', self.underline)
        self.text.bind('<Control-u>', self.underline)
        self.text.bind('<Control-T>', self.overstrike)
        self.text.bind('<Control-t>', self.overstrike)

class Font_Change(Note_Editor):
    """Create Class for Font"""
    def __init__(self, note_editor):
        self.top = Toplevel()
        self.top.title("Font")
        self.top.minsize(width=200, height=370)
        self.top.maxsize(width=200, height=370)

        label = Label(self.top, text="Please select a font...", width=30)
        label.pack()

        fonts = ("Arial","Courier New","Consolas","Clarendon","Comic Sans Ms",
                "MS Sans Serif","MS Serif","Times New Roman",
                "Serif","Symbol","System","Verdana")

        for font in fonts:
            Radiobutton(self.top, text=font, variable=note_editor.fontvar, value=font).pack(anchor=W)
        
        frame = Frame(self.top)
        frame.pack()
        applybutton = Button(frame, text="Apply", command=self.apply)
        applybutton.pack(side=LEFT)
        okbutton = Button(frame, text="   OK   ", command=self.ok)
        okbutton.pack(side=RIGHT)

        self.note_editor = note_editor

    def apply(self, *args):
        """Apply button function""" 
        self.note_editor.font = self.note_editor.fontvar.get()
        self.note_editor.text.config(font=(self.note_editor.font, self.note_editor.fontsize, self.note_editor.fontstyle))

    def ok(self, *args):
        """Ok button function"""
        self.note_editor.font = self.note_editor.fontvar.get()
        self.note_editor.text.config(font=(self.note_editor.font, self.note_editor.fontsize, self.note_editor.fontstyle))
        self.top.destroy()

class Font_Size(Note_Editor):
    """Create Class for Font Size"""
    def __init__(self, note_editor):
        self.top = Toplevel()
        self.top.title("Font Size")
        self.top.minsize(width=200, height=100)
        self.top.maxsize(width=200, height=100)

        label = Label(self.top, text="Please select a font size...", width=30)
        label.pack()

        self.scale = Scale(self.top, from_=10 , to=25, orient=HORIZONTAL)
        self.scale.pack()
        self.scale.set(note_editor.fontsize)

        frame = Frame(self.top)
        frame.pack()
        applybutton = Button(frame, text="Apply", command=self.apply)
        applybutton.pack(side=LEFT)
        okbutton = Button(frame, text="   OK   ", command=self.ok)
        okbutton.pack(side=RIGHT)
        
        self.note_editor = note_editor

    def apply(self, *args):
        """Apply button function"""
        self.note_editor.fontsize = self.scale.get()
        self.note_editor.text.config(font=(self.note_editor.font, self.note_editor.fontsize, self.note_editor.fontstyle))

    def ok(self, *args):
        """Ok button function"""
        self.note_editor.fontsize =self.scale.get()
        self.note_editor.text.config(font=(self.note_editor.font, self.note_editor.fontsize, self.note_editor.fontstyle))
        self.top.destroy()    

class SearchDialog(SearchDialogBase):
    """Create Class For Find Function"""
    def create_widgets(self, *args):
        SearchDialogBase.create_widgets(self)
        self.make_button("Find Next", self.default_command)
  
    def default_command(self, event=None, *args):
        self.find_function(self.text)

    def find_function(self, text, *args):
        """Find Function"""
        res = self.engine.search_text(text)
        if res:
            line, m = res
            l, j = m.span()
            first = "%d.%d" % (line, l)
            last = "%d.%d" % (line, j)
            try:
                selfirst = text.index("sel.first")
                sellast = text.index("sel.last")
                if selfirst == sellast and sellast == last:
                    self.bell()
                    return False
            except TclError:
                pass
            text.tag_remove("sel","1.0","end")
            text.tag_add("sel", first, last)
            text.mark_set("insert", self.engine.isback() and first or last)
            text.see("insert")
            return True
        if not res:
            self.bell()
            return False

class ReplaceDialog(SearchDialogBase):
    """Create Class For Replace Function"""
    title = "Replace Dialog"
    def __init__(self, root, engine, *args):
        SearchDialogBase.__init__(self, root, engine)
        self.replvar = StringVar(root)

    def open(self, text, *args):
        SearchDialogBase.open(self, text)
        try:
            first = text.index("sel.first")
        except TclError:
            first = None
        try:
            last = text.index("sel.last")
        except TclError:
            last = None
        first = first or text.index("insert")
        last = last or last
        self.show_hit(first, last)
        self.ok = 1               

    def create_entries(self, *args):
        SearchDialogBase.create_entries(self)
        self.replent = self.make_entry("Replace With:", self.replvar)[0]

    def create_command_buttons(self, *args):
        SearchDialogBase.create_command_buttons(self)
        self.make_button("Find", self.find_it)
        self.make_button("Replace", self.replace)
        self.make_button("Replace+Find", self.default_command, 1)
        self.make_button("Replace All", self.replace_all)   

    def find_it(self, event=None, *args):
        """Find Function"""
        self.do_find(0)

    def default_command(self, event=None, *args):
        """Replace+Find Function"""
        self.replace()
        self.do_find(0)

    def replace(self, event=None, *args):
        """Replace Function"""
        prog = self.engine.getprog()
        if not prog:
            return False
        repl = self.replvar.get()    
        text = self.text
        res = self.engine.search_text(text, prog)
        if not res:
            self.bell()
            return False
        first = last = None
        if res:
            line, m = res
            orig = m.group()
            new = self._replace_expand(m, repl)
            i, j = m.span()
            first = "%d.%d" % (line, i)
            last = "%d.%d" % (line, j) 
            if new == orig:
                text.mark_set("insert", last)
            else:
                text.mark_set("insert", first)
                if first != last:
                    text.delete(first, last)
                if new:
                    text.insert(first, new)
        if first and last:
            self.show_hit(first, last)

    def replace_all(self, event=None, *args):
        """Replace All Function"""
        prog = self.engine.getprog()
        if not prog:
            return
        repl = self.replvar.get() 
        text = self.text
        res = self.engine.search_text(text, prog)
        if not res:
            self.bell()
            return
        line = res[0]
        col = res[1].start()
        ok = 1
        first = last = None
        while True:
            res = self.engine.search_forward(text, prog, line, col, ok) 
            if not res:
                break
            line , m = res
            orig = m.group()
            new = self._replace_expand(m, repl) 
            if new is None:
                break
            i, j = m.span()
            first = "%d.%d" % (line, i)
            last = "%d.%d" % (line, j)
            if new == orig:
                text.mark_set("insert",last)
            else:
                text.mark_set("insert",first)
                if first != last:
                    text.delete(first, last) 
                if new:
                    text.insert(first, new)      
        if first and last:
            self.show_hit(first, last)
        self.close()                

    def _replace_expand(self, m, repl, *args):
        if self.engine.isre():
            try:
                new = m.expand(repl)
            except re.error:
                self.engine.report_error(repl, "Invalid Replace Expression")
                new = None
        else:
            new = repl
        return new                                                                  
 
    def do_find(self, ok=0, *args):
        text = self.text
        res = self.engine.search_text(text, None, ok)
        if not res:
            self.bell()
            return False
        line, m = res
        l, j = m.span()
        first = "%d.%d" % (line, l)
        last = "%d.%d" % (line, j)             
        self.show_hit(first, last)
        self.ok = 1
        return False

    def show_hit(self, first, last, *args):
        text = self.text
        text.mark_set("insert", first)
        text.tag_remove("sel","1.0","end")
        text.tag_add("sel", first, last)
        text.tag_remove("hit","1.0","end")
        if first == last:
            text.tag_add("hit", first)
        else:
            text.tag_add("hit", first, last)
        text.see("insert")
        text.update_idletasks()

def setup(text):
    """Create window for Find"""
    root = text._root()
    engine = searchengine.get(root)
    if not hasattr(engine, "_searchdialog"):
        engine._searchdialog = SearchDialog(root, engine)
    return engine._searchdialog

def find(text):
    pat = text.get("sel.first","sel.last")
    return setup(text).open(text, pat)

def replace(text):
    """Create window for Replace"""
    root = text._root()
    engine = searchengine.get(root)
    if not hasattr(engine,"_replacedialog"):
        engine._replacedialog = ReplaceDialog(root, engine)
    dialog = engine._replacedialog
    dialog.open(text)   

def main():
    try:
        root = Tk()
        note = Note_Editor(root)
        note.shortcut_keys()
        root.wm_state('zoomed')
        while True:
            root.update()
            if exit:
                root_close = True
    except TclError:
        pass        

if __name__=='__main__':
    main()