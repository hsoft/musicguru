#import <Cocoa/Cocoa.h>
#import <cocoalib/Outline.h>
#import "DetailsPanel.h"
#import "DesignWindow.h"
#import "LocationPanel.h"

@interface AppDelegate : NSObject
{
    IBOutlet PyMusicGuru *py;
    IBOutlet NSMenuItem *unlockMenuItem;
    
    DesignWindow *_designWindow;
    DetailsPanel *_detailsPanel;
    LocationPanel *_locationPanel;
}
/* Actions */
- (IBAction)addLocation:(id)sender;
- (IBAction)openWebsite:(id)sender;
- (IBAction)redirectToBoard:(id)sender;
- (IBAction)removeLocation:(id)sender;
- (IBAction)showDesignBoard:(id)sender;
- (IBAction)showDetails:(id)sender;
- (IBAction)showIgnoreBox:(id)sender;
- (IBAction)showLocations:(id)sender;
- (IBAction)unlockApp:(id)sender;
- (IBAction)updateCollection:(id)sender;

/* Public */
- (BOOL)canMaterialize;
- (SEL)getBoardActionForTag:(int)aTag;

/* Properties */
- (DetailsPanel *)detailsPanel;
- (PyMusicGuru *)py;
@end
