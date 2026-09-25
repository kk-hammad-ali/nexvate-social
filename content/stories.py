"""NEXVATE launch-30 daily Instagram & Facebook Stories.

The plan: "Daily Stories push traffic to the day's feed post." Every day gets:

  am    09:00 GST, a standalone frame built to be saved into a Highlight.
        One idea, taken from that day's post or the matching service page.
  push  30 min after the feed post, "New on the feed" with the day's tile.
        Short-lived: it's never added to a Highlight.
  ask   Days 7 and 19 only, the plan's poll and quiz. The API can't add
        poll/quiz stickers, so this background frame is posted by hand from
        the app, with the sticker added there.

Highlights are built from the am frames. The API can't create or edit
Highlights, so they're assembled by hand in the app from the Story archive:

  About     who we are and how we work
  Services  one frame per service, all 11 by day 24
  Tips      save-worthy advice from the education posts
  Process   how we scope, what we build with, who we suit
  Work      Bayline, our own product
  Book      the free audit, discovery call, open slots and contact

As in posts.py, every claim comes from nexvate.ae or the plan. Nothing is invented.
"""

WA = "+971 55 167 7805"

HIGHLIGHTS = ["About", "Services", "Tips", "Process", "Work", "Book"]

# day -> am frame. hl = the Highlight it's saved to, kicker = small label,
# then title, and either body or items, plus an optional foot line.
AM = {
    1: dict(hl="About", kicker="About · Nexvate", title="Build.<br>Launch.<br>Grow.",
            body="A UAE digital studio. We build the product — and the pipeline that sells it."),
    2: dict(hl="About", kicker="About · One team", title="Three agencies. Or one team.",
            items=["Apps, websites, stores & automation", "SEO, Google Ads & Meta Ads", "One plan. One team that owns the result."]),
    3: dict(hl="Services", kicker="Services · Overview", title="11 services.<br>Two jobs.",
            items=["Build — apps, web, Shopify, WordPress, AI, UI/UX, maintenance",
                   "Grow — SEO, Google Ads, Meta Ads, consulting"]),
    4: dict(hl="Services", kicker="Services · Mobile apps", title="Your app.<br>On both stores.",
            items=["Flutter, React Native or native", "App Store & Google Play submission", "Source code is yours"]),
    5: dict(hl="Tips", kicker="Tip · Speed", title="Slow on a phone? They've already left.",
            body="Compress images, cut plugins, and test on mobile data — not office Wi-Fi."),
    6: dict(hl="Services", kicker="Services · SEO", title="Be the answer when they search.",
            items=["Technical audit + ranked fix list", "Google Business Profile & local SEO", "Fixes implemented — not just listed"]),
    7: dict(hl="Tips", kicker="Tip · Contact", title="Contacting you should take one tap.",
            body="A WhatsApp button, not a number buried in the footer. One clear action on every page."),
    8: dict(hl="Services", kicker="Services · Custom web", title="Software that fits how you work.",
            items=["Booking & reservation systems", "Customer and partner portals", "Dashboards and internal tools"]),
    9: dict(hl="Process", kicker="Process · Scoping", title="How we scope a project",
            items=["01  Discovery call", "02  Written scope — including what's not included", "03  Fixed price & delivery plan"]),
    10: dict(hl="Services", kicker="Services · Meta Ads", title="Ads that start conversations.",
             items=["Pixel & Conversions API, set up properly", "Creative produced and tested", "Monthly cost-per-result report"]),
    11: dict(hl="Tips", kicker="Tip · Google Ads", title="Track conversions before you spend.",
             body="If Google doesn't know what a lead looks like, it optimises for clicks. Track calls, forms and WhatsApp taps first."),
    12: dict(hl="Services", kicker="Services · Shopify", title="Shopify stores built to sell in the UAE.",
             items=["UAE payment gateways & buy-now-pay-later", "Cash on delivery & local shipping", "Migration from WooCommerce or Magento"]),
    13: dict(hl="Book", kicker="Free · Audit", title="A free 15-minute website & growth audit.",
             items=["No pitch deck", "No obligation", "Just a straight answer"], foot=f"WhatsApp {WA}"),
    14: dict(hl="Process", kicker="Process · Stack", title="The stack follows the problem.",
             items=["Apps — Flutter, React Native, Swift, Kotlin", "Web — Laravel, Shopify, WordPress",
                    "AI — WhatsApp Business API, OpenAI, n8n"]),
    15: dict(hl="Services", kicker="Services · WordPress", title="A WordPress site your team can edit.",
             items=["Custom theme or block templates", "WooCommerce stores & checkout", "30 days of post-launch support"]),
    16: dict(hl="Tips", kicker="Tip · WhatsApp", title="In the UAE, the enquiry starts on WhatsApp.",
             body="If nobody answers for hours, they message the next business. Answer in seconds — at 2 a.m. too."),
    17: dict(hl="Services", kicker="Services · Google Ads", title="Paid search, judged on cost per lead.",
             items=["Account audit & restructure", "Conversion tracking that matches real leads", "You own the ad account"]),
    18: dict(hl="Services", kicker="Services · AI & automation", title="WhatsApp bots that know when to hand over.",
             items=["WhatsApp Business API chatbots", "Assistants trained on your own information", "Human hand-off, so nobody gets stuck"]),
    19: dict(hl="Tips", kicker="Tip · Reporting", title="Judge ads by cost per lead.",
             body="Impressions and clicks are clues, not results. The number that matters is what each lead costs you."),
    20: dict(hl="Work", kicker="Work · Bayline", title="Meet Bayline.",
             body="Our own garage management software for UAE workshops. Job cards, bookings, invoices and parts stock in one record.",
             foot="bayline.nexvate.ae"),
    21: dict(hl="Book", kicker="Free · Discovery call", title="Not sure what to build, fix or stop?",
             items=["Platform & vendor selection", "A prioritised roadmap", "A review of your current agency"],
             foot="Free discovery call — link in bio"),
    22: dict(hl="Services", kicker="Services · UI/UX", title="Design developers can build from.",
             items=["Wireframes & clickable prototypes", "Every state — not just the happy path", "A design system in Figma"]),
    23: dict(hl="Tips", kicker="Tip · Launch", title="A backup you've never restored is a hope.",
             body="Before launch: submit every form, test on a real phone, check tracking fires, and restore a backup once."),
    24: dict(hl="Services", kicker="Services · Maintenance", title="A named person who answers when it breaks.",
             items=["Scheduled updates", "Daily offsite backups — restores tested", "Uptime & security monitoring"]),
    25: dict(hl="Process", kicker="Process · Fit", title="Who we work best with",
             items=["UAE businesses with something real to sell", "Owners who want one accountable team",
                    "People who judge by leads, not likes"]),
    26: dict(hl="About", kicker="About · How we work", title="How we work",
             items=["A written scope before we start", "A fixed price, agreed up front",
                    "Code and ad accounts in your name", "Reports on leads, not impressions"]),
    27: dict(hl="Book", kicker="Booking · November", title="November project slots are open.",
             body="We plan our work a month ahead. Want to start in November? Now's the time to talk."),
    28: dict(hl="Tips", kicker="Tip · Build vs. buy", title="Build or buy?",
             items=["Online store → Shopify", "Marketing site → WordPress", "Bookings, portals, workflows → Custom",
                    "Customer app → Flutter / native"]),
    29: dict(hl="Work", kicker="Work · Bayline", title="7 WhatsApp follow-ups. Sent for you.",
             body="Bayline sends service reminders, car-ready alerts, review requests and payment chases from the workshop's own number."),
    30: dict(hl="Book", kicker="Contact", title="Let's build your next project.",
             items=["nexvate.ae/contact", f"WhatsApp {WA}", "info@nexvate.ae"]),
}

# The plan's two Story days. Options go on the poll/quiz sticker in the app.
ASK = {
    7: dict(kind="Poll", title="What's blocking your growth online?",
            options=["Website", "Getting leads", "Ads", "Time"]),
    19: dict(kind="Quiz", title="Which service would move the needle?",
             options=["A new website", "SEO", "Google / Meta Ads", "Automation"]),
}
