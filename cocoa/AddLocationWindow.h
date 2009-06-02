/* AddLocationWindow */

#import <Cocoa/Cocoa.h>

@interface AddLocationWindow : NSWindowController
{
    IBOutlet NSBox *fixedBox;
    IBOutlet NSBox *itunesBox;
    IBOutlet NSTextField *locationNameText;
    IBOutlet NSTextField *locationPathText;
    IBOutlet NSMatrix *locationTypeSelector;
    IBOutlet NSBox *removeableBox;
    IBOutlet NSTableView *removeableMediaTable;
    
    NSString *_currentPath;
    id _delegate;
    NSArray *_mediaList;
}
- (id)initWithDelegate:(id)aDelegate;

- (IBAction)addLocation:(id)sender;
- (IBAction)choosePath:(id)sender;
- (IBAction)locationTypeChange:(id)sender;

- (NSString *)locationNameFromPath:(NSString *)aPath;
- (void)onMountOrUnmount:(NSNotification *)notification;

//Properties
- (NSString *)currentPath;
- (void)setCurrentPath:(NSString *)aPath;
@end

@interface NSObject (AddLocationWindowDelegate)
//return @"" if everything is ok, or the error message if not.
- (NSString *)addLocationWithPath:(NSString *)aPath name:(NSString *)aName removeable:(BOOL)aRemoveable;
@end
