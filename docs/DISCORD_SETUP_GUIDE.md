# 🎮 Complete Discord Setup Guide for Switch
> **Step-by-Step Walkthrough to Run Your Multi-Agent War Room in Discord**

Follow these 4 simple steps to connect Discord to Switch and spawn your `@auditor`, `@metrics`, `@coder`, and `@dev` agents directly in your server.

---

## 🛠️ Step 1: Create Your Discord Bot in 2 Minutes

1. Go to the **[Discord Developer Portal](https://discord.com/developers/applications)** and sign in.
2. Click **"New Application"** in the top right.
   - Name it: `Agent Switch` (or `FinOps War Room`).
3. In the left sidebar, click **"Bot"**:
   - Click **"Reset Token"** (or "View Token") and **Copy the Bot Token**.
   - Save this token securely (you'll paste it into Switch Console).
4. Scroll down on the **Bot** page to **Privileged Gateway Intents**:
   - ✅ Toggle **ON**: `Server Members Intent`
   - ✅ Toggle **ON**: `Message Content Intent` *(Critical: without this, the bot cannot read message text!)*
   - Click **"Save Changes"** at the bottom.

---

## 🔗 Step 2: Invite the Bot to Your Discord Server

1. In the left sidebar, go to **OAuth2** ➔ **URL Generator**.
2. Under **Scopes**, select:
   - ✅ `bot`
   - ✅ `applications.commands` *(Enables native `/` slash commands)*
3. Under **Bot Permissions**, select:
   - ✅ **View Channels**
   - ✅ **Send Messages**
   - ✅ **Send Messages in Threads**
   - ✅ **Manage Webhooks** *(Critical: lets each agent post under its own avatar and name!)*
   - ✅ **Manage Channels**
   - ✅ **Manage Roles**
   - ✅ **Read Message History**
   - ✅ **Attach Files**
4. Copy the generated **Invite URL** at the bottom of the page.
5. Paste it into your browser, select your Discord server, and click **Authorize**.

---

## 🆔 Step 3: Copy Your Discord Server ID (Guild ID)

1. In your Discord app, open **User Settings** (gear icon bottom left) ➔ **Advanced** (under App Settings).
2. Toggle **ON** `Developer Mode`.
3. Right-click on your Discord server's icon in the server list on the left ➔ click **"Copy Server ID"**.

---

## ⚡ Step 4: Connect Discord in Switch Console & Deploy Room

### Option A: Using Switch Console (Desktop App)
1. Open **Switch Console**.
2. Select your server in the sidebar and open **Home** ➔ **Messaging Apps**.
3. Click **"Connect"** ➔ Select **Discord**.
4. Fill in:
   - **Name:** Your Server Name (e.g. `My Team Discord`)
   - **Bot Token:** *(Pasted from Step 1)*
   - **Guild ID:** *(Pasted from Step 3)*
5. Click **"Connect"**. Switch connects immediately.
6. Link your personal account: When prompted, select your Discord handle and click **"This is me"**.

### Deploying the FinOps Room:
1. In Switch Console, go to **Templates** ➔ **Import Template**.
2. Select [`finops-cost-optimizer.template.yaml`](./workflows/finops-cost-optimizer/finops-cost-optimizer.template.yaml).
3. Under **Messaging Bridge**, select your newly connected Discord.
4. Click **"Create Room & Spawn Agents"**.
5. Switch will automatically:
   - Create `#finops-cost-optimizer` in your Discord server.
   - Add `@auditor`, `@metrics`, `@coder`, and `@dev`.
   - Post the initial audit kickoff message!

---

### Option B: Turning an Existing Discord Channel into a Room
1. In Discord, create a new text channel: `#finops-war-room`.
2. Post an ordinary message in it (e.g. `Hello Switch!`).
3. Open Switch Console ➔ the channel appears under **"Your Rooms"**.
4. Invite your agents into the room with `/invite-agent` or via Switch Console.

---

## 🎯 Verification: Testing in Discord
In your Discord channel:
- Type `/` to see Switch slash commands auto-complete.
- Type:
  ```
  @auditor run weekly cloud spend audit
  ```
- Watch `@auditor` reply using its own name and webhook avatar, followed by `@metrics`, `@coder`, and `@dev`!
