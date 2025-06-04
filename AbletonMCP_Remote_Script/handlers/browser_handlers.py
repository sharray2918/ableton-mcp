"""Browser handlers for AbletonMCP Remote Script."""

import traceback
from typing import Any

from ..utils import BaseHandler


class BrowserHandlers(BaseHandler):
    """Handlers for browser-related commands."""

    def get_browser_item(self, uri: str | None, path: str | None) -> dict[str, Any]:
        """Get a browser item by URI or path"""
        try:
            # Access the application's browser instance instead of creating a new one
            app = self.control_surface.application()
            if not app:
                raise RuntimeError("Could not access Live application")

            result = {"uri": uri, "path": path, "found": False}

            # Try to find by URI first if provided
            if uri:
                item = self._find_browser_item_by_uri(app.browser, uri)
                if item:
                    result["found"] = True
                    result["item"] = {
                        "name": item.name,
                        "is_folder": item.is_folder,
                        "is_device": item.is_device,
                        "is_loadable": item.is_loadable,
                        "uri": item.uri,
                    }
                    return result

            # If URI not provided or not found, try by path
            if path:
                # Parse the path and navigate to the specified item
                path_parts = path.split("/")

                # Determine the root based on the first part
                current_item = None
                if path_parts[0].lower() == "instruments":
                    current_item = app.browser.instruments
                elif path_parts[0].lower() == "sounds":
                    current_item = app.browser.sounds
                elif path_parts[0].lower() == "drums":
                    current_item = app.browser.drums
                elif path_parts[0].lower() == "audio_effects":
                    current_item = app.browser.audio_effects
                elif path_parts[0].lower() == "midi_effects":
                    current_item = app.browser.midi_effects
                else:
                    # Default to instruments if not specified
                    current_item = app.browser.instruments
                    # Don't skip the first part in this case
                    path_parts = ["instruments", *path_parts]

                # Navigate through the path
                for i in range(1, len(path_parts)):
                    part = path_parts[i]
                    if not part:  # Skip empty parts
                        continue

                    found = False
                    for child in current_item.children:
                        if child.name.lower() == part.lower():
                            current_item = child
                            found = True
                            break

                    if not found:
                        result["error"] = f"Path part '{part}' not found"
                        return result

                # Found the item
                result["found"] = True
                result["item"] = {
                    "name": current_item.name,
                    "is_folder": current_item.is_folder,
                    "is_device": current_item.is_device,
                    "is_loadable": current_item.is_loadable,
                    "uri": current_item.uri,
                }

            return result
        except Exception as e:
            self.log_message("Error getting browser item: " + str(e))
            self.log_message(traceback.format_exc())
            raise

    def load_browser_item(self, track_index: int, item_uri: str) -> dict[str, Any]:
        """Load a browser item onto a track by its URI"""
        try:
            track = self.get_track(track_index)

            # Access the application's browser instance instead of creating a new one
            app = self.control_surface.application()

            # Find the browser item by URI
            item = self._find_browser_item_by_uri(app.browser, item_uri)

            if not item:
                raise ValueError(f"Browser item with URI '{item_uri}' not found")

            # Select the track
            self._song.view.selected_track = track

            # Load the item
            app.browser.load_item(item)

            return {
                "loaded": True,
                "item_name": item.name,
                "track_name": track.name,
                "uri": item_uri,
            }
        except Exception as e:
            self.log_message(f"Error loading browser item: {str(e)}")
            self.log_message(traceback.format_exc())
            raise

    def get_browser_tree(self, category_type: str = "all") -> dict[str, Any]:
        """
        Get a simplified tree of browser categories.

        Args:
            category_type: Type of categories to get ('all', 'instruments', 'sounds', etc.)

        Returns:
            Dictionary with the browser tree structure
        """
        try:
            # Access the application's browser instance instead of creating a new one
            app = self.control_surface.application()
            if not app:
                raise RuntimeError("Could not access Live application")

            # Check if browser is available
            if not hasattr(app, "browser") or app.browser is None:
                raise RuntimeError("Browser is not available in the Live application")

            # Log available browser attributes to help diagnose issues
            browser_attrs = [attr for attr in dir(app.browser) if not attr.startswith("_")]
            self.log_message(f"Available browser attributes: {browser_attrs}")

            result = {
                "type": category_type,
                "categories": [],
                "available_categories": browser_attrs,
            }

            # Helper function to process a browser item and its children
            def process_item(item: Any, depth: int = 0) -> dict[str, Any] | None:
                if not item:
                    return None

                result: dict[str, Any] = {
                    "name": item.name if hasattr(item, "name") else "Unknown",
                    "is_folder": hasattr(item, "children") and bool(item.children),
                    "is_device": hasattr(item, "is_device") and item.is_device,
                    "is_loadable": hasattr(item, "is_loadable") and item.is_loadable,
                    "uri": item.uri if hasattr(item, "uri") else None,
                    "children": [],
                }

                return result

            # Process based on category type and available attributes
            if (category_type == "all" or category_type == "instruments") and hasattr(app.browser, "instruments"):
                try:
                    instruments = process_item(app.browser.instruments)
                    if instruments:
                        instruments["name"] = "Instruments"  # Ensure consistent naming
                        result["categories"].append(instruments)
                except Exception as e:
                    self.log_message(f"Error processing instruments: {str(e)}")

            if (category_type == "all" or category_type == "sounds") and hasattr(app.browser, "sounds"):
                try:
                    sounds = process_item(app.browser.sounds)
                    if sounds:
                        sounds["name"] = "Sounds"  # Ensure consistent naming
                        result["categories"].append(sounds)
                except Exception as e:
                    self.log_message(f"Error processing sounds: {str(e)}")

            if (category_type == "all" or category_type == "drums") and hasattr(app.browser, "drums"):
                try:
                    drums = process_item(app.browser.drums)
                    if drums:
                        drums["name"] = "Drums"  # Ensure consistent naming
                        result["categories"].append(drums)
                except Exception as e:
                    self.log_message(f"Error processing drums: {str(e)}")

            if (category_type == "all" or category_type == "audio_effects") and hasattr(app.browser, "audio_effects"):
                try:
                    audio_effects = process_item(app.browser.audio_effects)
                    if audio_effects:
                        audio_effects["name"] = "Audio Effects"  # Ensure consistent naming
                        result["categories"].append(audio_effects)
                except Exception as e:
                    self.log_message(f"Error processing audio_effects: {str(e)}")

            if (category_type == "all" or category_type == "midi_effects") and hasattr(app.browser, "midi_effects"):
                try:
                    midi_effects = process_item(app.browser.midi_effects)
                    if midi_effects:
                        midi_effects["name"] = "MIDI Effects"
                        result["categories"].append(midi_effects)
                except Exception as e:
                    self.log_message(f"Error processing midi_effects: {str(e)}")

            # Try to process other potentially available categories
            for attr in browser_attrs:
                if attr not in [
                    "instruments",
                    "sounds",
                    "drums",
                    "audio_effects",
                    "midi_effects",
                ] and (category_type == "all" or category_type == attr):
                    try:
                        item = getattr(app.browser, attr)
                        if hasattr(item, "children") or hasattr(item, "name"):
                            category = process_item(item)
                            if category:
                                category["name"] = attr.capitalize()
                                result["categories"].append(category)
                    except Exception as e:
                        self.log_message(f"Error processing {attr}: {str(e)}")

            self.log_message(
                "Browser tree generated for {} with {} root categories".format(category_type, len(result["categories"]))
            )
            return result

        except Exception as e:
            self.log_message(f"Error getting browser tree: {str(e)}")
            self.log_message(traceback.format_exc())
            raise

    def get_browser_items_at_path(self, path: str) -> dict[str, Any]:
        """
        Get browser items at a specific path.

        Args:
            path: Path in the format "category/folder/subfolder"
                 where category is one of: instruments, sounds, drums, audio_effects, midi_effects
                 or any other available browser category

        Returns:
            Dictionary with items at the specified path
        """
        try:
            # Access the application's browser instance instead of creating a new one
            app = self.control_surface.application()
            if not app:
                raise RuntimeError("Could not access Live application")

            # Check if browser is available
            if not hasattr(app, "browser") or app.browser is None:
                raise RuntimeError("Browser is not available in the Live application")

            # Log available browser attributes to help diagnose issues
            browser_attrs = [attr for attr in dir(app.browser) if not attr.startswith("_")]
            self.log_message(f"Available browser attributes: {browser_attrs}")

            # Parse the path
            path_parts = path.split("/")
            if not path_parts:
                raise ValueError("Invalid path")

            # Determine the root category
            root_category = path_parts[0].lower()
            current_item = None

            # Check standard categories first
            if root_category == "instruments" and hasattr(app.browser, "instruments"):
                current_item = app.browser.instruments
            elif root_category == "sounds" and hasattr(app.browser, "sounds"):
                current_item = app.browser.sounds
            elif root_category == "drums" and hasattr(app.browser, "drums"):
                current_item = app.browser.drums
            elif root_category == "audio_effects" and hasattr(app.browser, "audio_effects"):
                current_item = app.browser.audio_effects
            elif root_category == "midi_effects" and hasattr(app.browser, "midi_effects"):
                current_item = app.browser.midi_effects
            else:
                # Try to find the category in other browser attributes
                found = False
                for attr in browser_attrs:
                    if attr.lower() == root_category:
                        try:
                            current_item = getattr(app.browser, attr)
                            found = True
                            break
                        except Exception as e:
                            self.log_message(f"Error accessing browser attribute {attr}: {str(e)}")

                if not found:
                    # If we still haven't found the category, return available categories
                    return {
                        "path": path,
                        "error": f"Unknown or unavailable category: {root_category}",
                        "available_categories": browser_attrs,
                        "items": [],
                    }

            # Navigate through the path
            for i in range(1, len(path_parts)):
                part = path_parts[i]
                if not part:  # Skip empty parts
                    continue

                if not hasattr(current_item, "children"):
                    return {
                        "path": path,
                        "error": "Item at '{}' has no children".format("/".join(path_parts[:i])),
                        "items": [],
                    }

                found = False
                for child in current_item.children:
                    if hasattr(child, "name") and child.name.lower() == part.lower():
                        current_item = child
                        found = True
                        break

                if not found:
                    return {
                        "path": path,
                        "error": f"Path part '{part}' not found",
                        "items": [],
                    }

            # Get items at the current path
            items = []
            if hasattr(current_item, "children"):
                for child in current_item.children:
                    item_info = {
                        "name": child.name if hasattr(child, "name") else "Unknown",
                        "is_folder": hasattr(child, "children") and bool(child.children),
                        "is_device": hasattr(child, "is_device") and child.is_device,
                        "is_loadable": hasattr(child, "is_loadable") and child.is_loadable,
                        "uri": child.uri if hasattr(child, "uri") else None,
                    }
                    items.append(item_info)

            result = {
                "path": path,
                "name": current_item.name if hasattr(current_item, "name") else "Unknown",
                "uri": current_item.uri if hasattr(current_item, "uri") else None,
                "is_folder": hasattr(current_item, "children") and bool(current_item.children),
                "is_device": hasattr(current_item, "is_device") and current_item.is_device,
                "is_loadable": hasattr(current_item, "is_loadable") and current_item.is_loadable,
                "items": items,
            }

            self.log_message(f"Retrieved {len(items)} items at path: {path}")
            return result

        except Exception as e:
            self.log_message(f"Error getting browser items at path: {str(e)}")
            self.log_message(traceback.format_exc())
            raise

    def _find_browser_item_by_uri(
        self,
        browser_or_item: Any,
        uri: str,
        max_depth: int = 10,
        current_depth: int = 0,
    ) -> Any:
        """Find a browser item by its URI"""
        try:
            # Check if this is the item we're looking for
            if hasattr(browser_or_item, "uri") and browser_or_item.uri == uri:
                return browser_or_item

            # Stop recursion if we've reached max depth
            if current_depth >= max_depth:
                return None

            # Check if this is a browser with root categories
            if hasattr(browser_or_item, "instruments"):
                # Check all main categories
                categories = [
                    browser_or_item.instruments,
                    browser_or_item.sounds,
                    browser_or_item.drums,
                    browser_or_item.audio_effects,
                    browser_or_item.midi_effects,
                ]

                for category in categories:
                    item = self._find_browser_item_by_uri(category, uri, max_depth, current_depth + 1)
                    if item:
                        return item

                return None

            # Check if this item has children
            if hasattr(browser_or_item, "children") and browser_or_item.children:
                for child in browser_or_item.children:
                    item = self._find_browser_item_by_uri(child, uri, max_depth, current_depth + 1)
                    if item:
                        return item

            return None
        except Exception as e:
            self.log_message(f"Error finding browser item by URI: {str(e)}")
            return None
