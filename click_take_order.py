from click_button import click_button

# Wait for and click the TAKE ORDER button
clicked = click_button("assets/take_order_template.png", threshold=0.85)
