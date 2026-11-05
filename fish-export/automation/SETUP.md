# n8n setup checklist

## In each workflow
Open the **Config** node and set the brand, the emails, `waPhoneNumberId`, `salesWhatsApp` and `sheetId`. Workflow 05 already points at the WBF_Exporter_List sheet. Then attach the credentials marked `REPLACE_ME`.

## HubSpot
- Create a private app with these scopes: `crm.objects.contacts.read/write`, `crm.objects.deals.read/write` and `crm.objects.companies.write`. In n8n, add it as a *HubSpot App Token* credential.
- Create two contact properties as single-line text with **Unique value** ticked: `whatsapp_id` and `messenger_psid`.
- Set `hubspotPipeline` and `hubspotStage` in Config. The defaults are `default` and `appointmentscheduled`.

## WhatsApp Cloud API (Meta)
- Create a permanent System User token and add it in n8n as *Header Auth*: `Authorization: Bearer <token>`.
- Submit these templates for approval (category Utility, language `en`):
  - `rfq_received`: "Hi {{1}}, thank you for your quote request {{2}}. Our team will send your price offer within 24 hours."
  - `new_lead_alert`: "New {{1}} lead: {{2}}. Products: {{3}}. Ref {{4}}."
- Webhook: callback URL `…/webhook/wbf-meta`. The verify token must match `VERIFY_TOKEN` in the "Check verify token" node. Subscribe to `messages`.

## Messenger
- Add a Page access token as *Header Auth* and subscribe the Page webhook to `messages`.

## Email and Sheets
- Add an SMTP credential.
- RFQ, chat and event logs: create a Google Sheet with three tabs named `RFQ`, `Chats` and `Events`, and put its ID in `sheetId` for workflows 01–03.
- Supplier applications (workflow 05) go to the `Exporter List` tab of WBF_Exporter_List. Columns match by header name.

## Production
- Set the webhooks' `allowedOrigins` to your domain instead of `*`.
- Paste each workflow's production webhook URL into `CONFIG` in `assets/js/site.js`.
