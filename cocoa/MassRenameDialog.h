/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "PyMusicGuru.h"

@interface MassRenameDialog : NSWindowController
{
    IBOutlet NSTextField *customModelText;
    IBOutlet NSMatrix *modelSelector;
    IBOutlet NSTextField *nameAfterLabel;
    IBOutlet NSTextField *nameBeforeLabel;
    IBOutlet NSMatrix *whitespaceSelector;
    
    PyMassRenamePanel *py;
}
- (id)initWithPyMassRenamePanel:(PyMassRenamePanel *)aPy;
- (void)dealloc;

- (IBAction)cancel:(id)sender;
- (IBAction)changeExampleSong:(id)sender;
- (IBAction)displayExampleSong:(id)sender;
- (IBAction)ok:(id)sender;

- (BOOL)run;
@end
