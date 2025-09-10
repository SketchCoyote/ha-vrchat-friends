# **VRChat Friends Integration for Home Assistant**

A Home Assistant integration that tracks your VRChat friends, providing rich presence information to power your automations and dashboards.

This integration creates a sensor that shows how many of your friends are currently in-game, and provides a detailed list of those friends as an attribute.

## **Features**

* **Real-time Friend Count:** A sensor that shows the number of friends currently in-game.  
* **Rich Attributes:** Provides a detailed online\_list attribute containing each friend's:  
  * Display Name  
  * Current Status (Join Me, Ask Me, Busy)  
  * Status Description  
  * Profile Picture & Current Avatar URLs  
  * Current Location & Platform Data  
* **Smart Filtering:** Automatically filters out friends who are only "active" on the VRChat website, showing you only those who are truly in-world.  
* **Easy Configuration:** A simple UI-based setup process. No YAML editing required for configuration.

## **Installation**

### **Prerequisites**

You must have [HACS (Home Assistant Community Store)](https://hacs.xyz/) installed on your Home Assistant instance to use this integration.

### **Installation via HACS (Recommended)**

1. Go to **HACS** in your Home Assistant.  
2. Click on **Integrations**.  
3. Click the three-dots menu in the top-right corner and select **"Custom repositories"**.  
4. Add the URL to this repository and select the **"Integration"** category.  
5. Find the "VRChat Friends" integration in the list and click **"Download"**.  
6. Restart Home Assistant.

### **Manual Installation**

1. Download the latest release from the [Releases](https://www.google.com/search?q=https://github.com/your_github_username/ha-vrchat-friends/releases) page on GitHub.  
2. Unzip the downloaded file.  
3. Copy the vrchat folder (from within the custom\_components folder) into your Home Assistant's custom\_components directory.  
4. Restart Home Assistant.

## **Configuration**

Once installed, the integration can be configured through the Home Assistant UI.

1. Go to **Settings \> Devices & Services**.  
2. Click the **"+ Add Integration"** button.  
3. Search for **"VRChat Friends"** and click on it.  
4. You will be prompted to enter your VRChat Authentication Cookie.

### **How to get your VRChat Authentication Cookie**

The authentication cookie is required for the integration to securely access your friends list.

1. Log in to the [VRChat Website](https://vrchat.com/) in a web browser (like Chrome or Firefox).  
2. Open your browser's **Developer Tools**. You can usually do this by pressing **F12** or right-clicking the page and selecting "Inspect".  
3. Go to the **Application** tab (in Chrome) or **Storage** tab (in Firefox).  
4. On the left side, under "Storage", expand the "Cookies" section and select https://vrchat.com.  
5. Find the cookie named **auth**.  
6. Copy the **entire value** from the "Cookie Value" column. It's a very long string of text.  
7. Paste this entire string into the configuration prompt in Home Assistant.

## **Usage**

This integration creates a single sensor:

* **sensor.vrchat\_friends\_in\_world**:  
  * The **state** of the sensor is the number of friends currently in-game.  
  * The **online\_list** attribute contains a detailed list of all online friends, which you can use in automations and custom dashboard cards.

### **Example Automation**

You can use the online\_list attribute to create powerful automations, such as sending a notification when a specific friend comes online.

### **Example Lovelace Card**

You can create a beautiful dashboard card to display your online friends. This example requires the [HTML Jinja2 Template Card](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-Jinja2-Template-card) from HACS.

type: custom:html-template-card  
title: VRChat Friends In-World  
content: |  
  {% set friends \= state\_attr('sensor.vrchat\_friends\_in\_world', 'online\_list') %}  
  {% if friends and friends | length \> 0 %}  
    {% for friend in friends %}  
      \<\!-- Your custom HTML and Jinja2 logic here \--\>  
    {% endfor %}  
  {% else %}  
    No friends are currently in-world.  
  {% endif %}

## **Contributions**

Contributions are welcome\! If you have suggestions or find a bug, please [open an issue](https://www.google.com/search?q=https://github.com/your_github_username/ha-vrchat-friends/issues).

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
