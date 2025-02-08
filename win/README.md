# Windows Tips

## Allow Anonymous Access to Shared Folder or Printer on Windows 10

By default, when you access a shared folder on a remote computer, you are prompted for a username and password (except in cases where both computers are in the same domain, or workgroup and use the same local user accounts with the same passwords). Anonymous access means that when you connect to a remote computer, you are not prompted for a password and can access shared resources without authentication.

In most cases, opening anonymous access to shared network folders is not recommended for security reasons. Anonymous access allows any unauthenticated user to read, modify, or delete files in a shared folder. Guest access is recommended for exceptional use in a secure network perimeter.

### Configuring Anonymous Access Settings in Windows

Windows uses a special built-in guest account for anonymous access. This account is disabled by default.

To allow anonymous (unauthenticated) access to the computer, you need to enable the `Guest` account and change some settings of the Local Security Policy in Windows.

Open the Local Group Policy Editor console (`gpedit.msc`) and navigate `Computer Configuration -> Windows Settings -> Security Settings -> Local Policies -> Security Options`

- Accounts: `Guest Account Status`: Enabled
- Network access: `Let Everyone permissions apply to anonymous users`: Enabled
- Network access: `Do not allow anonymous enumeration of SAM accounts and shares`: Disabled
- Then make sure that `Guest` or `Everyone` is also specified in the `Access this computer from network` policy and the `Deny access to this computer from the network` policy should not have `Guest` as the value.

For security reasons, it is also a good idea to open the `Deny log on locally` policy under the `Local Policies -> User Rights Assignment` to ensure that the Guest account is specified in the policy settings.

Also, make sure that network folder sharing is enabled under `Settings -> Network & Internet -> Ethernet -> Change advanced sharing options`. Check that `Turn on file and printer sharing`, `Network Discovery` (allows to show computers in the network environment) are enabled, and `Turn off password protected sharing option` is disabled in all network profile sections (Private, Public, All networks).
