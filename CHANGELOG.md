# Changelog

## [1.3.0] - 2024-03-21
### Changed
- Replaced individual target ID variables with a single `TARGET_USER_IDS` list
- Added comments to identify each user in the target IDs list

## [1.2.0] - 2024-03-21
### Added
- Added initial deafened user check on bot startup
- New `check_deafened_users()` function to scan all guilds for deafened target users

## [1.1.0] - 2024-03-21
### Added
- Added detailed logging for voice state updates
- Added new case to handle channel changes while deafened
- Extracted move logic into separate `move_to_shadow_realm` function

### Changed
- Improved voice state update handling to check deafen state in three scenarios:
  1. When user first joins a voice channel
  2. When user moves between voice channels
  3. When user toggles deafen state while in a channel

## [1.0.0] - 2024-03-21
### Added
- Initial bot implementation
- Basic voice state monitoring for target users
- Shadow Realm channel detection and movement
- Deafened state detection and handling 