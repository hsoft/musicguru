<%!
	title = 'Building your collection'
	selected_menu_item = 'Build'
%>
<%inherit file="/base_mg.mako"/>

musicGuru manages your music collection through locations. A location is simply a place where you have music files. For example, your iTunes directory may be added as a location, as well as each of your CDs containing music files. It is important to note that locations in the musicGuru database are **virtual**. When you add, for example, a CD to your musicGuru database, files are not copied on your computer. musicGuru just read each file to record metadata (like artist/album/genre/etc..).

The first time you start musicGuru, there is no location in its database. The first thing you need to do is to add a location. You can do so with **Menu|Build|Add Location**.

Adding songs
-----

When you click on **Menu|Build|Add Location**, an Add Location dialog will pop, and the first thing you will have to do is to indicate the source of the songs you want to add.

**Choosing a source type**

You have basically two choices here: Add songs from a fixed drive (hard disk, internal or external) or from a removable media (CD/DVD). When you add a fixed location, this location will be updated when you perform the **Update Collection** function and when you open the design board. When you add a removable location, it will never be updated, and when musicGuru will need files from this drive (when materializing a collection), you will be prompted for this media.

**Telling musicGuru where that source is**

Below the source type selector is a box where you must specify the exact location of the songs you want to add. The nature of that box depends of what source type you selected.

* The iTunes option is a shortcut doing the same thing as the fixed drive option.
* If you chose the fixed drive option, you will have to indicate a path where your songs are. You can click on "Choose" and choose the path of your to-be-added location.
* If you chose the removable media option, you will have a list of all currently inserted removable medias, and you will have to choose one among them.

**Choosing a location name**

The location name field at the bottom of the window will change as you select source type and specify your song source. You can change that name before adding your location if you want. However, you can't have two locations with the same name.

**Letting musicGuru work**

When you click **Add Location**, musicGuru will start the real thing. It will read each song's metadata and add it to its database.

Updating Collection
-----

Your collection on fixed drive(s) is likely to change over time. This is why the **Update Collection** feature exists. You can launch it by clicking on **Menu|Build|Update Collection**. The **Update Collection** feature simply compare it's database with your hard drive(s) and updates what needs to be updated. You have nothing to do, just wait until it's finished updating.

Unreachable locations
-----

When a fixed location can't be reached by musicGuru (external drive unplugged, directory moved), the location name will be red and you will not be able to materialize a design containing that location. To be able to materialize your design, plug your external drive in, or change its path with the "Change" button next to the path in the location window.

Color codes
-----

* **Black:** Fixed location.
* **Blue:** Removable location.
* **Red:** Unreachable location.
