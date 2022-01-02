from AppKit import NSApplication, NSApp, NSWorkspace
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo
from Cocoa import NSApplicationActivateIgnoringOtherApps, NSApplicationActivateAllWindows

def setActiveWindow(title):
    workspace = NSWorkspace.sharedWorkspace()
    activeApps = workspace.runningApplications()
    for app in activeApps:
        if title in '%s' % app.localizedName():
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps | NSApplicationActivateAllWindows)