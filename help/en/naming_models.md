The **Mass Rename** and **Split into CD/DVD** features of the [Design Board](design.htm) both feature the possibility for you to define your own naming model.

A naming model is a line of text containing **tokens**. A **token** is a word enclosed in two **%** signs. For example, **%artist%** is a token. A **token** can also have one or more **parameters**. A parameter is a word, following the token, but within the **%** signs, that is preceded with a **:** sign. For example, **%item:first%** is a token with one parameter and **%group:artist:elp:lower%** is a token with 3 parameters. Few tokens in musicGuru take parameters. In fact, only **item** and **group**.

So, what do these tokens do? They are placeholders for names that will change depending on the file that is processed. Everything that is not a token will always stay the same, and a **/** sign indicate a directory separator. For example, if you **Mass Rename** 3 files: "The White Stripes - Elephant - Seven Nation Army", "Modest Mouse - The Moon and Antartica - 3rd Planet" and "The White Stripes - Get Behind Me Satan - Forever For Her" (all very nice songs) with the model **%artist%/hello - %album%/%title%**, you will have 2 root directories: "Modest Mouse" and "The White Stripes". Under "Modest Mouse", you will have 1 directory, "hello - The Moon and Antartica", and in that directory, 1 song, "3rd Planet". Under "The White Stripes", you will have 2 directories, "hello - Elephant" and "hello - Get Behind Me Satan", which will respectively have "Seven Nation Army" and "Forever For Her" in them.

You don't have to care about the extension of your files when you create your renaming model, musicGuru automatically adds it.

**Mass Rename** and **Split into CD/DVD** have a different set of tokens. You can't use **Mass Rename** tokens in **Split into CD/DVD** and vice versa.

Mass Rename tokens
-----

<table class="hardcoded">
    <tr class="header"><td>Token</td><td>Is replaced by...</td></tr>
    <tr><td>%artist%</td><td>Song's artist</td></tr>
    <tr><td>%album%</td><td>Song's album</td></tr>
    <tr><td>%year%</td><td>Song's year</td></tr>
    <tr><td>%genre%</td><td>Song's genre</td></tr>
    <tr><td>%track%</td><td>Song's track</td></tr>
    <tr><td>%title%</td><td>Song's title</td></tr>
    <tr>
        <td>%extension%</td>
        <td>Song's extension. You do not need to put it at the end of each model (in fact, you must not), musicGuru does that automatically. However, you might want your songs to be organized by extension. You would then use the token in a directory name.
        </td>
    </tr>
    <tr>
        <td>%oldpath%</td>
        <td>Song's path (without the file name) before the renaming.</td>
    </tr>
    <tr>
        <td>%oldfilename%</td>
        <td>Song's file name before the renaming.</td>
    </tr>
    <tr>
        <td>%group:group_by:steps:case%</td>
        <td>The song's attribute "group_by" in a format "A-Z". "steps" determine the ranges of the groups. "case" determines whether the result is lowercase or uppercase. The default for "steps" is "emp", and the default for "case" is "upper". Nothing is better than a little example to explain. %groups:album:emp% would create 4 directories (if there are songs belonging to every group): "A-D", "E-L", "M-O","P-Z". Every directory will contain songs having their album with their first letter in the range. If you change the steps, the result will be different. You can have more or less than 3 character in the "steps" parameter. If you set "case" to "lower", the result will be lowercase.</td>
    </tr>
</table>

Split into CD/DVD tokens
-----

<table class="hardcoded">
    <tr class="header"><td>Token</td><td>Is replaced by...</td></tr>
    <tr>
        <td>%sequence%</td>
        <td>CD's sequence, starting with 1</td>
    </tr>
    <tr>
        <td>%item:which:letter%</td>
        <td>
            One of the CD's sub item. Depending on the "which" parameter, it can either be the first or the last. You guessed it, the possible values for "which" is "first" or "last". "letter" is optional. If "letter" is not present, the whole item name will be returned. If letter is present, it must be a number. The number typed there will be the number of letters that will be displayed. For example, if the letter = 1, only the first letter of the item will be displayed. If letter = 2, the 2 first letters will be displayed etc..
        </td>
    </tr>
</table>
