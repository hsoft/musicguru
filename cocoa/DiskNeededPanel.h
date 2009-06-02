/* DiscNeededPanel */

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
