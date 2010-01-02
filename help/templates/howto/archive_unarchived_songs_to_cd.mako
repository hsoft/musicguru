<%!
	title = "How to archive songs that aren't archived yet"
	selected_menu_item = 'How To'
%>
<%inherit file="/base_mg.mako"/>

So what you basically want to do is to add your collection on your hard drive at the same time as your CDs, mass rename everything, and remove all conflicts. For this purpose, the Move Conflicts feature doesn't work because it leaves the original there. This is why we will use Move Conflicts *and* Original. As said in [this How To](merge_music_collections.htm), the duplicate detection mechanism of musicGuru isn't very advanced yet, but it will be once Mp3 Filter 5 is out because musicGuru will intergrate features from it. Meanwhile, what you can do to detect duplicates that aren't found by the conflicts mechanism is to look at the Location column of your top level directories. If the column indicate that there are songs from both hard drive and CD locations in it, it is a good evidence that there might be duplicates in this folder, so you can investigate further.

1. [Build your collection](build_music_collection.htm) and don't forget to add your CDs to it!
1. Click on **Design Board**.
1. Click on the checkbox next to you hard drive location in the **Locations pane**.
1. Click on the checkbox next to each of your CD locations.
1. In the menu, click on **Design|Mass Rename**.
1. Click on **OK**.
1. Click on **Menu|Design|Move Conflicts *and* Original**.
1. Uncheck your CD locations to remove them from the design board.
1. There might be some inconsistencies in the **Mass Rename** result due to inconsistent tags. You can merge directories together by dragging a directory's content in another directory.
1. Click on **Split into CD/DVD**.
1. Select a CD naming model.
1. If you really want to record as few CD as possible, leave the **Grouping level** slider at the extreme left. But if you want to prevent your artists from being splitted, put the slider on the second tick.
1. Click on **OK**
1. Because you already have some recorded CD, you might have to manually rename your CDs. If, for example, your naming model is a sequence and you already have 7 recorded CDs, then you would have to rename your CDs so the sequence starts at 8.
1. Click on **Materialize**.
1. Select **Record renamed songs to CD/DVD**.
1. Click on **Next**.
1. Review your to-be-recorded CDs and recording options and click on **Next**.
1. From now on, musicGuru will prompt you for a blank CD when it needs it. Just follow the instructions until you get a screen telling you that you are finished.
1. Click on **Finish**.
