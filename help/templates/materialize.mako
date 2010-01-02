<%!
	title = 'Materializing your design'
	selected_menu_item = 'Materialize'
%>
<%inherit file="/base_mg.mako"/>

You should now be finished perfecting your collection design, and you just clicked on **Materialize** in the design board. The **Materialize** feature is a wizard, and the first screen gives you the choice between the 4 basic types of materialization.

Rename songs in their respective location
-----

This will simply perform the naming operation required to create your design. All songs will be kept in their respective location. That is, if you have 2 locations in your design board, songs won't be mixed between them. Of course, you can't do this with locations from removable media. If you had such a location in your board, it will simply be ignored. When you choose this option and click **Next**, the operation will start right away, as it needs no further configuration.

Move songs in a single location
-----

This will move all songs from the design board in the same location. If you included a location from a removable media, you will be prompted for it during the operation, and the songs will be **copied** from it instead of moved. This operation is usually used when you have songs in 2 or more locations that you want to merge together, so you can remove on of them. When you will click **Next**, you will be prompted for a location to move the songs to. You can either choose an existing location, or create a new one. Then, when clicking **Next** again, the operation will start.

Copy songs in a single location
-----

This is quite like **Move renamed songs in one location**, except that **everything** is copied instead of moved, not just the removable medias.

Record songs to CD/DVD (OS X only)
-----

This will record your design board into CDs or DVDs. You **must** have used the **Split into CD/DVD** feature to use this option. The first screen after clicking **Next** is a screen giving 2 options, as well as a summary of the to-be-recorded CDs. The first option is **Add recorded Cds to your collection**. If you select it, there will be one location created in your musicGuru database for each CD recorded. The second option is **Recorded CDs overwrite any location with the same name**. musicGuru can't have 2 location with the same name. Thus, if you select this option and one of the recorded CDs have the same name as an existing location, the new location from the recorded CD will overwrite the old one. If you don't select the option, no new location will be added if there is a conflict.

musicGuru has a very nice buffering feature, which let's you re-design your CD collection, even if your hard disk does not have enough space to hold them all. If you record a design that has some location from removable media, musicGuru will copy songs from these media **on-the-fly** into a buffer, and delete them from the buffer as soon as they are recorded. That means that you only need as much free disk space as your recorded CD/DVD with the most data coming from removable media.

If your design board have one or more location from a removable media, you will then have a screen giving you a summary of your available disk space. You can't continue if you don't have enough free disk space.

When you will click on **Next**, the recording process will start. For every recorded CD, the actual recording process will or will not be preceded by a song fetching process, prompting you for source CDs, depending on if the recorded CD need or doesn't need songs from removable medias. musicGuru optimizes the song fetching process to prompt you for the same CD as few times as possible, depending on your available disk space. If you have at least the recommended available disk space, you will never be prompted more than once for the same CD. After the optional song fetching phase, the actual recording phase will start, prompting you to insert a blank CD in your drive. 

If you use the buffering system and have limited available disk space, try not to download or copy stuff on your disk, it might disturb the buffering process. The buffer only use a part of your available space, so it will not be a problem if you only download small stuff, but if you download big enough stuff to take some of the buffer's space, it might disturb the process.
