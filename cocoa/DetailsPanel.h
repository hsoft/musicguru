/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "../cocoalib/PyApp.h"
#import "../cocoalib/Table.h"


@interface DetailsPanel : NSWindowController
{
    IBOutlet TableView *detailsTable;
}
- (id)initWithPy:(PyApp *)aPy;

- (void)refresh;
@end