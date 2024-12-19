#!/usr/bin/env python3

import salt.client

def check_for_updates():
    """
    Checks for available updates on the system using Salt's pkg module.

    Returns:
        dict: A dictionary containing the number of available updates and details if possible.
              Returns None on error.
    """
    local = salt.client.LocalClient()

    try:
        # Detect the OS family to use appropriate commands
        os_family = local.cmd('*', 'grains.get', ['os_family'])[list(local.cmd('*', 'grains.get', ['os_family']).keys())[0]]['os_family']
    
        updates = {}
        
        if os_family == 'RedHat':
            # Use pkg.list_upgrades for Red Hat based systems (CentOS, Fedora, etc.)
            upgrades = local.cmd('*', 'pkg.list_upgrades')

            for minion, pkgs in upgrades.items():
                updates[minion] = {
                    'count': len(pkgs),
                    'details': pkgs
                }

        elif os_family == 'Debian':
            # Use pkg.list_upgrades for Debian based systems (Debian, Ubuntu, etc.)
            upgrades = local.cmd('*', 'pkg.list_upgrades')
            
            for minion, pkgs in upgrades.items():
              updates[minion] = {
                  'count': len(pkgs),
                  'details': pkgs
              }

        elif os_family == 'Suse':
            # Use pkg.list_upgrades for SUSE based systems (SLES, openSUSE)
            upgrades = local.cmd('*', 'pkg.list_upgrades')

            for minion, pkgs in upgrades.items():
                updates[minion] = {
                    'count': len(pkgs),
                    'details': pkgs
                }

        elif os_family == 'Arch':
            # Use pkg.list_upgrades for Arch based systems.
            upgrades = local.cmd('*', 'pkg.list_upgrades')

            for minion, pkgs in upgrades.items():
                updates[minion] = {
                    'count': len(pkgs),
                    'details': pkgs
                }

        else:
            print(f"Unsupported OS family: {os_family}")
            return None

        return updates

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    update_info = check_for_updates()

    if update_info:
        for minion, info in update_info.items():
            if info['count'] > 0:
                print(f"Minion: {minion}")
                print(f"  Number of updates available: {info['count']}")
                print(f"  Details: {info['details']}")
            else:
                print(f"Minion: {minion}")
                print(f"  No updates available at this time.")
    else:
        print("Could not retrieve update information.")
