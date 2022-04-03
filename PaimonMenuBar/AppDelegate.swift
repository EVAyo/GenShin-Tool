//
//  AppDelegate.swift
//  PaimonMenuBar
//
//  Created by Spencer Woo on 2022/3/23.
//

import AppKit
import Foundation
import SwiftUI

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!

    private lazy var contentView: NSView? = {
        let view = (statusItem.value(forKey: "window") as? NSWindow)?.contentView
        return view
    }()

    @objc private func openSettingsView() {
        NSApp.sendAction(Selector(("showPreferencesWindow:")), to: nil, from: nil)
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
        NSApp.windows.first?.makeKeyAndOrderFront(self)
    }

    func applicationDidFinishLaunching(_: Notification) {
        // Update game record on initial launch
        Task {
            await GameRecordViewModel.shared.updateGameRecord()
        }

        // Close main APP window on initial launch
        NSApp.setActivationPolicy(.accessory)
        if let window = NSApplication.shared.windows.first {
            window.close()
        }

        setupStatusItem()
        setupMenus()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_: NSApplication) -> Bool {
        // Hide app icon in dock after all windows are closed
        NSApp.setActivationPolicy(.accessory)
        return false
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: 100)

        let hostingView = NSHostingView(rootView: MenuBarResinView())
        hostingView.translatesAutoresizingMaskIntoConstraints = false
        guard let contentView = contentView else { return }
        contentView.addSubview(hostingView)

        NSLayoutConstraint.activate([
            hostingView.topAnchor.constraint(equalTo: contentView.topAnchor),
            hostingView.rightAnchor.constraint(equalTo: contentView.rightAnchor),
            hostingView.bottomAnchor.constraint(equalTo: contentView.bottomAnchor),
            hostingView.leftAnchor.constraint(equalTo: contentView.leftAnchor),
        ])
    }

    private func setupMenus() {
        let menu = NSMenu()

        // Main menu area, render view as NSHostingView
        let menuItem = NSMenuItem()
        GameRecordViewModel.shared.hostingView = NSHostingView(rootView: AnyView(MenuExtrasView()))
        GameRecordViewModel.shared.hostingView?.frame = NSRect(x: 0, y: 0, width: 280, height: 425)
        menuItem.view = GameRecordViewModel.shared.hostingView
        menu.addItem(menuItem)

        // Submenu, preferences, and quit APP
        menu.addItem(NSMenuItem.separator())
        menu
            .addItem(NSMenuItem(title: String(localized: "Preferences"), action: #selector(openSettingsView),
                                keyEquivalent: ","))
        menu
            .addItem(NSMenuItem(title: String(localized: "Quit"), action: #selector(NSApplication.terminate(_:)),
                                keyEquivalent: "q"))

        statusItem.menu = menu
    }
}
