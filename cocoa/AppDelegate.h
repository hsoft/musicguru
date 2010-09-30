/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "Outline.h"
#import "DetailsPanel.h"
#import "DesignWindow.h"
#import "LocationPanel.h"

@interface AppDelegate : NSObject
{
    IBOutlet PyMusicGuru *py;
    
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
- (IBAction)updateCollection:(id)sender;

/* Public */
- (BOOL)canMaterialize;
- (SEL)getBoardActionForTag:(int)aTag;

/* Properties */
- (DetailsPanel *)detailsPanel;
- (PyMusicGuru *)py;
@end
