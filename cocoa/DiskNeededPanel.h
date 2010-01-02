/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>

@interface DiskNeededPanel : NSWindowController
{
    IBOutlet NSTextField *messageLabel;
    IBOutlet NSButton *okButton;
    IBOutlet NSTableView *volumeTable;
    
    NSArray *_mediaList;
    BOOL _running;
}
+ (NSString *)promptForDiskNamed:(NSString *)aDiskName;

- (IBAction)cancel:(id)sender;
- (IBAction)ejectSelected:(id)sender;
- (IBAction)ok:(id)sender;

- (NSString *)promptForDiskNamed:(NSString *)aDiskName;
- (void)onMountOrUnmount:(NSNotification *)notification;
- (void)threadedMountCheck;
@end
