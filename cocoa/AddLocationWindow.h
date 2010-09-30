/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

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
