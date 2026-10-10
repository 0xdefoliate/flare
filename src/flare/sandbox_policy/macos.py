#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

POLICY_MAC_OS = """
;  Copyright (c) 2026 Axel H. Karlsson and contributors.
;
;  You may use the source-code in accordance with the licence found
;  in the LICENSE file, available in the project's root directory.

(version 1)
(deny default)

(import "system.sb")

; BEGIN NETWORK
; Copyright 2018 The Chromium Authors

; DNS configuration watcher entries. This is a nesty mess of symlinks.
(allow file-read*
    (path "/")
    (path "/etc")
    (path "/etc/hosts")
    (path "/etc/resolv.conf")
    (path "/private")
    (path "/private/etc")
    (path "/private/etc/hosts")
    (path "/private/etc/resolv.conf")
    (path "/private/var")
    (path "/private/var/run")
    (path "/private/var/run/resolv.conf")
    (path "/var")
    (path "/var/run")
)

; Network socket access.
(allow network-outbound
    (control-name "com.apple.netsrc")
    (literal "/private/var/run/mDNSResponder")
    (remote tcp)
    (remote udp)
)
; END NETWORK

; Note that this only allows reading metadata, not contents of files themselves.
; We'd rather remove this rule, since data can be leaked, but, without this rule,
; the program cannot resolve paths.
(allow file-read-metadata)

; These are needed for the Python binary to work.
;
; In theory, the "/System" and "/Library" paths could be more strict
; but I didn't have much time to sit with that.
(allow file-read*
    (literal "/")
    (subpath "/System")
    (subpath "/Library")
    (subpath "/usr/lib")
    (subpath "/usr/local/Cellar") ; might be a bit broad; might need some attention...
    (literal "/bin/realpath")
    (literal "/usr/bin/env")
    (literal "/usr/bin/python3")
    (subpath (param "PROJ_DIR"))
)

; TODO: Make these rules more specific as well!
(allow process-fork)
(allow process-exec)

; Required for ncurses
(allow file-ioctl (regex #"^/dev/ttys[0-9]+"))
"""