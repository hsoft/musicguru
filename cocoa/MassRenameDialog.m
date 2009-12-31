/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "MassRenameDialog.h"
#import "../cocoalib/Utils.h"

@implementation MassRenameDialog
- (id)initWithPyMassRenamePanel:(PyMassRenamePanel *)aPy
{
    self = [super initWithWindowNibName:@"MassRename"];
    py = [aPy retain];
    [self window]; //Initialize Widgets
    return self;
}

- (void)dealloc
{
    [py release];
    [super dealloc];
}

- (IBAction)cancel:(id)sender
{
    [NSApp stopModalWithCode:NSCancelButton];
    [[self window] close];
}

- (IBAction)changeExampleSong:(id)sender
{
    [py changeExampleSong];
    [self displayExampleSong:sender];
}

- (IBAction)displayExampleSong:(id)sender
{
    [py setModelSelectedRow:i2n([modelSelector selectedRow])];
    [py setWhitespaceSelectedRow:i2n([whitespaceSelector selectedRow])];
    [customModelText setEnabled:[modelSelector selectedRow] == 4];
    [nameBeforeLabel setStringValue:[py getExampleDisplayBefore]];
    [nameAfterLabel setStringValue:[py getExampleDisplayAfter]];
}

- (IBAction)ok:(id)sender
{
    [NSApp stopModalWithCode:NSOKButton];
    [[self window] close];
}

- (BOOL)run
{
    //Returns YES if OK was clicked, and NO otherwise.
    [self displayExampleSong:self];
    return ([NSApp runModalForWindow:[self window]] == NSOKButton);
}

//Delegate
- (void)controlTextDidChange:(NSNotification *)aNotification
{
    [py setCustomModel:[customModelText stringValue]];
    [self displayExampleSong:self];
}
@end
