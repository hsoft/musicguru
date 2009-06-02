#import "DetailsPanel.h"

@implementation DetailsPanel
- (id)initWithPy:(PyApp *)aPy
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