# Avalon Privacy Policy

Last updated: {{last_updated}}

Avalon is developed and provided by {{developer_name}}. This policy covers the Avalon Mac app and its included mobile browser access. It explains how your local library handles data and how we handle information when you contact support or visit this website.

## 1. Your library stays on your devices

Avalon manages photos and videos locally. Library data is stored on the Mac running Avalon, disks you select, or your chosen backup locations. Search models run on the Mac. The current version does not provide a developer-hosted cloud library or automatically upload your photos, videos, search queries or library to us or a third-party AI service.

Local processing does not mean data can never leave the Mac. Authorized local-network users, share links you create, and downloads, exports or backups you initiate may make content available on other devices or to other recipients.

## 2. Data processed locally and its purposes

- **Photos and videos**: Files in folders you select, and content you import or upload, are processed for browsing, playback, organization, downloads, exports and backups.
- **File and photo metadata**: This includes names, paths, sizes, timestamps, content checksums, disk and folder information, and existing EXIF such as camera details, capture time and GPS capture locations. It supports identification, deduplication, sorting, maps, search and backup management. Capture locations come from imported file metadata rather than continuous tracking of your current location.
- **Derived data**: Thumbnails, previews, search vectors, indices and generated album content support display, semantic search and album creation. Search models perform inference on the local library; the current version does not send this content to us for model training.
- **Accounts and library activity**: Usernames, password hashes, roles, sessions, permissions, favorites, tags, albums and share records support local-library sign-in, access control and your saved actions. The server's account database stores one-way password hashes. If you select Remember password in the Mac client, the sign-in password is separately stored in system secure storage (the macOS Keychain). App clients and mobile browsers retain the state needed to stay signed in, including essential session cookies for Web sign-in. A password-protected share page may retain the share password for the current browser session so it can survive a page refresh. These mechanisms enable sign-in and share access, not advertising tracking.
- **Runtime and diagnostic information**: Settings, versions, task status, a random installation identifier and runtime logs support startup, troubleshooting and local tasks. Logs may contain file paths, timestamps, errors and activity records and are not automatically sent to us. The app's Copy support information action copies only the version and platform, without automatically including photos, logs, paths or credentials.

The current release package does not provide face recognition. These descriptions do not mean this release builds face recognition templates. If this feature is introduced, we will update the information and provide appropriate settings.

## 3. Folder permissions and local-network access

You grant folder access through the system folder picker and can manage it in the app's Folder access settings. Applicable system permissions can also be managed in macOS System Settings. Revoking access limits future access but does not automatically erase existing thumbnails, indices, imported copies or backups.

Mobile browsers and other authorized users may connect to the Mac running Avalon and browse, upload or manage content according to library permissions. The library administrator manages accounts and permissions and controls local data. Grant access only to people you trust.

The current default local-network connection uses HTTP without transport encryption. Password hashing at rest does not encrypt sign-in requests or content in transit. Use a trusted network and do not expose service ports directly to the public internet. Network forwarding, proxies or remote access you configure yourself may change who can reach the library.

## 4. Sharing, exports and third parties

Share links may make selected content available to anyone holding the link. Recipients may download or retain copies. Choose content and recipients carefully and revoke shares when no longer needed. Revoking a link cannot retrieve copies already downloaded, captured or forwarded. Capture locations and other metadata may also be disclosed when you share original files.

The current Avalon app contains no advertising, advertising tracking or third-party behavioral analytics SDK and does not sell your library data. Software components support local display, storage and computation; importing a library does not automatically provide its contents to the developer.

Email services, websites, recipient devices and external storage services you choose handle information you send under their own rules. Apple provides operating-system and store services under its policies. Apple-managed diagnostics, downloads or payments are separate from automatic library uploads by Avalon.

## 5. Retention, deletion and withdrawal of access

Local data generally remains until you delete it, reset the library or manually remove the relevant files. Uninstalling the app may leave application data, source files, uploaded originals and backups behind.

- **Delete my account**: Request deletion in Privacy and support and confirm with your current password. The account is disabled and sessions are revoked immediately. Associated personal favorites, albums, tags, shares and permission records are subsequently cleaned up. Keep the Mac service running until background cleanup finishes. Shared originals, public metadata and shared indices remain under the Mac administrator's control and are not removed simply because an individual account is deleted.
- **Delete photos or videos**: Use file deletion and check the selected scope of files and copies. Offline disks, trash, independent backups and copies already sent to others may retain content and require separate checking or removal.
- **Reset local library**: After system authentication, the local administrator can remove library accounts, databases, search indices, thumbnails, share caches and logs and clear folder grants. Uploaded originals, selected source files and backups remain. Set up an administrator, grant folder access and import again afterwards.
- **Revoke access**: You can revoke folder grants or shares. Administrators manage accounts, sessions and library access. Revocation does not erase independent copies already created.

The developer cannot directly read or remotely delete your local library. Use the local controls or contact the library administrator for shared content. To request deletion of support information previously sent to us, contact the email below.

## 6. Information you send to support

When you contact {{contact_email}}, we receive the email address, description and attachments you choose to provide, solely to reply, investigate problems and handle requests. Prefer redacted error details and do not send passwords, session credentials, full private photos or your complete library.

Support correspondence is processed through your email provider and the service we use to receive email. We may keep correspondence while resolving the issue and for necessary follow-up, deleting it when no longer needed unless applicable law requires retention. You can request deletion of information you sent. We will verify the request and handle it within applicable legal deadlines.

## 7. Visits to this website

GitHub Pages hosts this privacy and support website. These pages add no analytics scripts, advertising, cookies, external fonts or third-party embeds. GitHub may still process network information such as IP addresses and access logs under its policies to deliver pages and operate the service. Visiting this website does not submit your Avalon library.

See the [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). External websites you visit through links have their own privacy policies.

## 8. Your choices and requests

Local controls let you view, download or export content, change library information, manage permissions, revoke shares and delete your account. The local administrator can reset the library. Respect other people's privacy and permissions when handling their photos or a shared library.

If your local law provides rights of access, correction, deletion, restriction, objection or data portability, you may contact us about information we hold. You or an authorized administrator must perform local-library actions. Withdrawing access does not affect processing already performed before withdrawal.

## 9. Changes and contact

When data practices or relevant features change, we will update this policy and its date. We will explain material changes through appropriate means and obtain authorization when required.

Developer: {{developer_name}}

Privacy and support email: [{{contact_email}}](mailto:{{contact_email}})
