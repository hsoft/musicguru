#import "PathChoicePage.h"
#import <cocoalib/Dialogs.h>

@implementation PathChoicePage

- (id)init
{
    self = [super init];
    [self setTitle:@"Destination Path"];
    return self;
}

- (IBAction)choosePath:(id)sender
{
    NSOpenPanel *op = [NSOpenPanel openPanel];
    [op setCanChooseFiles:NO];
    [op setCanChooseDirectories:YES];
    if ([op runModalForTypes:nil] == NSOKButton)
        [pathText setStringValue:[[op filenames] objectAtIndex:0]];
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    NSFileManager *fm = [NSFileManager defaultManager];
    NSString *path = [[pathText stringValue] stringByExpandingTildeInPath];
    if (![path length])
        @throw @"The path cannot be empty.";
    BOOL isDir;
    if ([fm fileExistsAtPath:path isDirectory:&isDir])
    {
        if (!isDir)
            @throw @"The path you chose is a file. You cannot use this path.";
    }
    else
    {
        if ([Dialogs askYesNo:@"This path does not exist, do you want to create it?"] == NSAlertFirstButtonReturn)
        {
            if (![fm createDirectoryAtPath:path attributes:nil])
                @throw @"Couldn't create the directory.";
        }
        else
            @throw @"The path you choose must be an existing directory.";
    }
    [aInfo setObject:path forKey:@"ChosenPath"];
}

@end
