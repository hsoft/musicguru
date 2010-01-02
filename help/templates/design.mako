<%!
	title = 'Designing your collection'
	selected_menu_item = 'Design'
%>
<%inherit file="/base_mg.mako"/>

Once you've built your musicGuru collection, the fun begins. With the musicGuru Design Board, you can painlessly re-design your collection. One thing about the Design Board is important to remember: **This is virtual. No changes are made to your actual collection until you click the Materialize button.**

What's the point of the Design Board?
-----

The Design Board lets you freely play around with the structure of your music collection. Thus, you can move files around, merge directories (even if they are from different locations!), send some unwanted files to the ignore box, split this all into 700, 4700 or 8500 MB chunks (to record them), and then, when you feel you have the perfect collection design, you can click on **Materialize** to make that perfect design come to reality.

Adding and removing locations to the board
-----

The first thing to do when you open the Design Board is to add some locations to it. The Design Board, like the main window, has a location pane. This pane is a little different than the other because each location has a checkbox next to it. Clicking on this checkbox adds or removes the location from the board (If the box was checked, it removes the location, if it wasn't, it adds it). The location addition process automatically merges directories of the same name, and automatically resolves conflicts. There are more details about this in the next section.

Playing with the board
-----

The central piece of the Design Board is the big browser in the middle of it. This widget displays the content of all locations added to the board. Directories have a little arrow next to them, which let's you expand or collapse their content.

**Renaming**

When you double-click on a file or directory, a text box will pop, allowing you to type a new name for the clicked file or directory. When you're finished typing the new name, you can click away or press return to perform the rename.

**Dragging around**

You can drag files and directory around, moving them at will. You can also drag from and to the ignore box. There is a special trick with dragging, and it is the **Command** key. If you hold the **Command** key when you **start** a drag operation, the selected item's **children** will be dragged. And if the same **Command** key if held when you **end** a drag operation (when you drop the thing), the dragged item(s) will be moved as **siblings** of the drop destination instead of its child.

For example, if you have 2 similar directories in your Design Board: "White Stripes" and "The White Stripes". You say to yourself "Hey! I want these directories merged!". You could expand the "White Stripes" directory, select all it's children, and drag them into the "The White Stripes" directory, but you could also hold **Command**, drag the "White Stripes" directory, release the **Command** key, and drop it into the "The White Stripes" directory.

**Creating Folders**

There is a feature in the **Design** menu called **New Folder**. Clicking on this menu item will create a new folder in the currently selected folder. If nothing is selected, the folder will be created directly in the design board. The created folder will automatically go in rename mode so you can type a new name right away.

**Removing empty folders**

There are good chances that you will end up with a lot of empty folders when you will design your collection. There is a feature in the **Design** menu called **Remove Empty Folders**. When you click on it, all empty folders are removed recursively.

**The Ignore Box**

Files cannot be removed individually from the design board. They can only be removed in bulk when you remove a location by unchecking it in the locations pane. However, they can be **ignored**. All files that are dragged into the ignore box will not be materialized. So this is quite like if they were removed, but you can still bring them back if you want.

**Conflicts**

When 2 files or more have the same name and are in the same directory, there is a naming conflict. When this happens, the conflictual file's name is prepended by [xxx] where xxx is a sequence (example: [000], [001], [002]). The parent directory (as well as grandparents) of a conflicted file gains a special icon with a red exclamation mark.

Having conflictual files does not prevent you from materializing your design, but it is not recommended, because it does not make a very graceful collection design. As soon as the conflict is gone, the little red mark goes away.

**The order in which you add locations to the design board is important** for automatic conflict resolution happening in Mass Rename. The sooner you add a location, the higher its files' priority will be in conflict resolution. That means that if you add location **A** before location **B** and the mass rename renames 2 files from each of these location to the same name, the file from location **B** will get the "conflicted" status.

**Switch Conflict And Original**

To create a conflict, it takes at least two songs. And among the songs creating a conflict, one of them will not be considered "conflicted". And sometimes, it isn't the right one. When it happens, just select the song that shouldn't be conflicted, and use this command. It is just a shortcut for renaming both songs.

**Move Conflicts**

This feature simply takes all conflicted files, and move them into a folder named "conflicts" in the ignore box. If for some reason, the song that created the conflict (and didn't get a conflicted name) isn't there anymore, the conflicted song will simply take it's place instead of going to the ignore box. There is a [How To page](howto/resolve_conflicts.htm) about resolving conflicts.

**Move Conflicts and Original**

Like **Move Conflicts**, but it also moves the song that wasn't renamed to a conflicted name (if it's still there and if it hasn't been renamed).

Now, let's get serious
-----

All the nice little features described above are handy for doing finition jobs, but the big job will probably be performed by the two big brothers described here, namely **Mass Rename** and **Split into CD/DVD**.

**Mass Rename**

The Mass Rename feature will re-organize all your design board according to a naming model you will give to it. When you click on **Menu|Design|Mass Rename**, a window will pop asking for a naming model. You can select one of the pre-defined ones, or you can make your own custom one. To design your own model, see the [Naming Models](naming_models.htm) section.

The popped window also lets you choose a whitespace policy. For example, you might have an inconsistent collection, and have some files with an Artist tag value of "The White Stripes", and some with an Artist tag value of "The_White_Stripes". If you select "Leave the as is", 2 directories will be created, and each file will be in it's own directory. If you select "Replace all whitespaces with underscores", all files will go under a single directory, named "The_White_Stripes". And if you select "Replace all underscores with a space character", all files will go under a single directory, named "The White Stripes".

At the bottom of the window, there is a preview of what the rename operation will look like. You can change the example song by clicking on "Change Example Song". A new, song will then be randomly chosen.

**Split into CD/DVD**

This feature is really nice. It will split your design board into chunks of pre-determined size. This will then allow you to use the CD/DVD recording feature of the **Materialize** wizard. You should be finished renaming and moving your files around before using this feature, because once the design board is split, it is more touchy to move files around (because you have to stay below your media capacity).

Like the **Mass Rename** feature, a window will pop when you click on **Split into CD/DVD**. Like with **Mass Rename** You have to choose a naming model for the to-be-created CDs. You can select a pre-defined model or make your own, after having read the [Naming Models](naming_models.htm) section.

Then you have to choose the size of the chunks you want to make. This, of course, all depends on what kind of recorder you have.

Ahh, the **grouping level**. Another niceness. If you try to split your board by letting the grouping level be at 0, you might notice that some artists and albums will end up on different CDs. If your absolute goal is to record your collection on as few CDs as possible, it is good. But otherwise, it's kind of a pain. If you move the **grouping level** slider one tick to the right, the level will be 1. And at 1, no directory will be split between CDs. This is nice, but it might lead you to record significantly more CDs. You can move the slider one more tick to the right, and have a grouping level of 2. In this case, top level directories **can** be split, but not their subdirectories. If you have an Artist/Album naming model, it means that you can have the same artist on 2 CDs, but never the same album. The righter is the slider, the smaller the groups will be. And if the slide is at the extreme left, no grouping will take place. If your grouping level is greater than the deepness of your directory structure, a "(No folder as this level)" message will be displayed, which means that no grouping will take place.
