# Version 0.91 - Linkedin Post Screenshot Generator

# Import the required libraries
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Constants
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 400
PROFILE_PHOTO_SIZE = 80
TEXT_PADDING = 20
PROFILE_PHOTO_PADDING = 10
FONT_SIZE = 22
SMALL_FONT_SIZE = 12
BOLD_FONT_SIZE = 24
FONT_COLOR = (0, 0, 0)  # Black
PROFILE_NAME = "John Doe"
ADDITIONAL_INFO = "Marketing Specialist and Content Creator"
LINKEDIN_LOGO_PATH = "linkedin_logo.png"  # Path to the LinkedIn logo image file
PROFILE_PHOTO_PATH = "profile_photo.png"  # Path to your profile photo image file

# Prompt for the post text
post_text = input("Enter the text for the post: ")

# Create a blank image
image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
draw = ImageDraw.Draw(image)

# Load system fonts
font = ImageFont.truetype("Arial", FONT_SIZE)
small_font = ImageFont.truetype("Arial", SMALL_FONT_SIZE)
bold_font = ImageFont.truetype("Arial Bold", BOLD_FONT_SIZE)

# Add text to the image
text_width, text_height = draw.textsize(post_text, font=font)
text_position = ((IMAGE_WIDTH - text_width) // 2, (IMAGE_HEIGHT - text_height) // 2)
draw.text(text_position, post_text, fill=FONT_COLOR, font=font)

# Load and resize the LinkedIn logo
linkedin_logo = Image.open(LINKEDIN_LOGO_PATH)
linkedin_logo = linkedin_logo.resize((PROFILE_PHOTO_SIZE, PROFILE_PHOTO_SIZE)).convert("RGBA")

# Create a white background image with the same size as the logo
background = Image.new("RGBA", linkedin_logo.size, (255, 255, 255))

# Overlay the logo on the white background
linkedin_logo_with_background = Image.alpha_composite(background, linkedin_logo)

# Load and resize your profile photo
profile_photo = Image.open(PROFILE_PHOTO_PATH)
profile_photo = profile_photo.resize((PROFILE_PHOTO_SIZE, PROFILE_PHOTO_SIZE))

# Create a circular mask for the profile photo
mask = Image.new("L", (PROFILE_PHOTO_SIZE, PROFILE_PHOTO_SIZE), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse((0, 0, PROFILE_PHOTO_SIZE, PROFILE_PHOTO_SIZE), fill=255)

# Apply the circular mask to the profile photo
profile_photo = ImageOps.fit(profile_photo, mask.size, centering=(0.5, 0.5))
profile_photo.putalpha(mask)

# Calculate positions for the logo and profile photo
logo_position = (IMAGE_WIDTH - PROFILE_PHOTO_SIZE - PROFILE_PHOTO_PADDING, PROFILE_PHOTO_PADDING)
photo_position = (PROFILE_PHOTO_PADDING, PROFILE_PHOTO_PADDING)

# Overlay the logo and profile photo on the image
image.paste(linkedin_logo_with_background, logo_position)
image.paste(profile_photo, photo_position, profile_photo)

# Calculate the width and height of the profile name text
name_width, name_height = draw.textsize(PROFILE_NAME, font=bold_font)

# Calculate the position to center the profile name vertically with reference to the profile photo
name_position = (
    photo_position[0] + PROFILE_PHOTO_SIZE + PROFILE_PHOTO_PADDING,
    photo_position[1] + (PROFILE_PHOTO_SIZE - (name_height + SMALL_FONT_SIZE + 10)) // 2
)

# Add your profile name next to the profile photo (in a bigger bold font)
draw.text(name_position, PROFILE_NAME, fill=FONT_COLOR, font=bold_font)

# Calculate the width and height of the additional information text
info_width, info_height = draw.textsize(ADDITIONAL_INFO, font=small_font)

# Calculate the position to place the additional information underneath the profile name
info_position = (
    name_position[0],
    name_position[1] + name_height + 10
)

# Add the additional information in small font
draw.text(info_position, ADDITIONAL_INFO, fill=FONT_COLOR, font=small_font)

# Save the final image
image.save("linkedin_post_screenshot.png")
