from stability_sdk import api
from stability_sdk.animation import AnimationArgs, Animator

STABILITY_HOST = ""
STABILITY_KEY = ""

context = api.Context(STABILITY_HOST, STABILITY_KEY)

# Configure the animation
args = AnimationArgs()
args.interpolate_prompts = True
args.locked_seed = True
args.max_frames = 48
args.seed = 42
args.strength_curve = "0:(0)"
args.diffusion_cadence_curve = "0:(4)"
args.cadence_interp = "film"

animation_prompts = {
    0: "a photo of a cute cat",
    24: "a photo of a cute dog",
}
negative_prompt = ""

# Create Animator object to orchestrate the rendering
animator = Animator(
    api_context=context,
    animation_prompts=animation_prompts,
    negative_prompt=negative_prompt,
    args=args
)

# # Render each frame of animation
# for idx, frame in enumerate(animator.render()):
#     frame.save(f"frame_{idx:05d}.png")

print(animator.render())

