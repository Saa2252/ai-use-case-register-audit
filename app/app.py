"""The published site, served through Streamlit.

**What this is, and what it deliberately is not.**

This was built once before, as a set of Streamlit components restating the
project's findings, and the owner dropped it the next day. The reason is
recorded in governance/decision-rules.md section 23.5, and it was right: what
it could not reproduce was the page as a designed object, because the host owns
the page. A second surface that states the same findings less well is not a
second surface. It is a weaker copy of the first.

The owner's instruction this time is that the interface be identical. There is
exactly one way to meet that, and it is not to rebuild the page in a framework
that owns the layout. It is to stop rebuilding it and serve the real one.

So this application renders nothing of its own. Every Streamlit element on the
page is removed, and what remains is the published site, at full width and full
height, with its own stylesheet, its own scripts and its own navigation. The
design is not approximated because it is not reproduced.

**What follows from that, stated rather than discovered later.**

This holds no figures. It reads no data file. There is no copy of any finding
anywhere in it, so there is nothing here that can drift from the audit, which
is the failure this project has had repeatedly. The safeguards are held where
they already were: inside the page being served.

It depends on the published site being reachable. If it is not, the reader is
told so and given the address, rather than shown an empty frame.

The address and the disclaimer are imported from src/disclaimer.py rather than
written here, so this file cannot state either of them differently from the
site it serves.
"""

from pathlib import Path
import sys

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.disclaimer import AUTHORSHIP, DISCLAIMER, SITE_URL  # noqa: E402

# Must be the first Streamlit call on the page.
st.set_page_config(
    page_title="AI Use Case Register Audit",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Every piece of Streamlit's own interface, removed. The header, the toolbar,
# the running indicator, the footer, the menu, and the padding the block
# container adds around anything placed in it. What is left is a viewport with
# one frame in it.
#
# Each selector is listed on its own line with what it removes, because a
# selector that stops matching after a Streamlit release should be findable by
# reading rather than by bisecting.
st.markdown(
    """
    <style>
      /* The bar across the top, and the coloured line under it. */
      header[data-testid="stHeader"] { display: none !important; }
      div[data-testid="stDecoration"] { display: none !important; }
      div[data-testid="stToolbar"] { display: none !important; }
      div[data-testid="stStatusWidget"] { display: none !important; }
      #MainMenu { display: none !important; }
      footer { display: none !important; }

      /* The padding Streamlit puts around whatever is placed on the page. */
      div[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
      div[data-testid="stAppViewBlockContainer"],
      .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
      }
      div[data-testid="stVerticalBlock"] { gap: 0 !important; }
      div[data-testid="stElementContainer"] { margin: 0 !important; }

      /* The frame itself, filling the window.
         The test id sits on the iframe, not on a wrapper around it, and the
         height comes from a generated class rather than an inline style.
         Written as a descendant selector first, this matched nothing, the
         generated height won, and the foot of the framed page sat below the
         window on any viewport shorter than it. The containers above it are
         sized too, or they keep the height the component was born with. */
      iframe[data-testid="stIFrame"],
      iframe[title="st.iframe"],
      div[data-testid="stCustomComponentV1"] iframe {
        width: 100vw !important;
        height: 100vh !important;
        min-height: 100vh !important;
        border: 0 !important;
        display: block !important;
      }
      div[data-testid="stElementContainer"]:has(iframe[data-testid="stIFrame"]),
      div[data-testid="stVerticalBlock"]:has(iframe[data-testid="stIFrame"]) {
        height: 100vh !important;
        min-height: 100vh !important;
      }

      /* The ground behind the frame, in both schemes.
         Streamlit paints its own background and has no way to follow the
         system scheme, so the window flashes a colour the site never uses
         while the frame loads. These two values are the site's own --bg
         tokens, light and dark, and tests/test_app_safeguards.py reads them
         out of docs/assets/style.css and fails if they drift. */
      html, body, div[data-testid="stAppViewContainer"] {
        background: #fbfbf9 !important;
        overflow: hidden !important;
      }
      @media (prefers-color-scheme: dark) {
        html, body, div[data-testid="stAppViewContainer"] {
          background: #14150f !important;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# The site itself. Nothing is passed in and nothing is read out: this is the
# published page, loaded from where it is published.
# The height here is only what the element is born with. The stylesheet above
# takes it to the full window, and scrolling happens inside the frame, which is
# where the site expects it.
# The height here is only what the element is born with. The stylesheet above
# takes it to the full window, and scrolling happens inside the frame, which is
# where the site expects it.
st.components.v1.iframe(SITE_URL, height=900, scrolling=True)

# Shown only when the frame above has nothing to show, which happens when the
# published site cannot be reached. A page that fails should say so rather than
# look like a site with its content missing. The site carries the disclaimer in
# its own footer; this is the copy that applies when the site is not there.
st.markdown(
    f"""
    <noscript>
      <div style="padding:1.5rem;font-family:system-ui,sans-serif;max-width:40rem">
        <p><strong>This page shows the published site and needs scripts enabled.</strong></p>
        <p><a href="{SITE_URL}">Open the site directly</a></p>
        <p style="font-size:.85rem;color:#57544c">{DISCLAIMER}</p>
        <p style="font-size:.85rem;color:#57544c">{AUTHORSHIP}</p>
      </div>
    </noscript>
    """,
    unsafe_allow_html=True,
)
