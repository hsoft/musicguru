/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "DetailsPanel.h"

@implementation DetailsPanel
- (id)initWithPy:(PyMusicGuru *)aPy
{
    self = [super initWithWindowNibName:@"Details"];
    [self window]; //So the detailsTable is initialized.
    [detailsTable setPy:aPy];
    return self;
}

- (void)refresh
{
    [detailsTable reloadData];
}
@end