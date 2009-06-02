//
//  main.m
//  musicguru_cocoa
//
//  Created by Virgil Dupras on 2006/01/24.
//  Copyright Hardcoded Software 2004-2006. All rights reserved.
//

#import <Cocoa/Cocoa.h>

int main(int argc, char *argv[])
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    NSString *pluginPath = [[NSBundle mainBundle]
                                pathForResource:@"mg_cocoa"
                                         ofType:@"plugin"];
    NSBundle *pluginBundle = [NSBundle bundleWithPath:pluginPath];
    [pluginBundle load];
    [pool release];
    return NSApplicationMain(argc,  (const char **) argv);
}
