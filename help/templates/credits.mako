<%!
	title = 'Credits'
	selected_menu_item = 'Credits'
%>
<%inherit file="/base_mg.mako"/>
Below is the list of people who contributed, directly or indirectly to musicGuru.

${self.credit('Virgil Dupras', 'Developer', "That's me, Hardcoded Software founder", 'www.hardcoded.net', 'hsoft@hardcoded.net')}

${self.credit('Python', 'Programming language', "The bestest of the bests", 'www.python.org')}

${self.credit('PyObjC', 'Python-to-Cocoa bridge', "Used for the Mac OS X version", 'pyobjc.sourceforge.net')}

${self.credit('Brian Lloyd', 'Python for .NET Author', "Python-to-.NET bridge (used for the Windows version)", 'sourceforge.net/projects/pythonnet/')}

${self.credit('Sparkle', 'Auto-update library', "Used for the Mac OS X version", 'andymatuschak.org/pages/sparkle')}

${self.credit('You', 'musicGuru user', "What would I do without you?")}
