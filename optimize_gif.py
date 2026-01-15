from PIL import Image
import os

def optimize_gif(input_path, output_path, max_size_mb=15, target_frames=None):
    """
    Optimize GIF file size by reducing frames, resolution, and quality.
    """
    # Open the GIF
    with Image.open(input_path) as img:
        frames = []
        durations = []

        # Read all frames
        try:
            while True:
                frames.append(img.copy())
                durations.append(img.info.get('duration', 100))  # Default 100ms
                img.seek(img.tell() + 1)
        except EOFError:
            pass

        print(f"Original GIF has {len(frames)} frames")

        # Reduce frame count if specified or if we have too many frames
        if target_frames and len(frames) > target_frames:
            # Sample frames evenly
            step = len(frames) // target_frames
            frames = frames[::step][:target_frames]
            durations = durations[::step][:target_frames]
            print(f"Reduced to {len(frames)} frames")

        # Reduce resolution if needed (start with 75% of original)
        original_size = frames[0].size
        new_size = (int(original_size[0] * 0.75), int(original_size[1] * 0.75))

        print(f"Resizing from {original_size} to {new_size}")
        resized_frames = []
        for frame in frames:
            resized_frames.append(frame.resize(new_size, Image.Resampling.LANCZOS))

        # Try different optimization approaches
        current_size = float('inf')
        best_frames = resized_frames
        best_durations = durations

        # First attempt: optimize with default settings
        temp_path = output_path + '.temp1.gif'
        best_frames[0].save(
            temp_path,
            save_all=True,
            append_images=best_frames[1:],
            duration=best_durations,
            loop=0,
            optimize=True,
            quality=85
        )
        current_size = os.path.getsize(temp_path) / (1024 * 1024)  # Size in MB
        print(f"First attempt: {current_size:.2f} MB")

        # If still too large, reduce quality further
        if current_size > max_size_mb:
            os.remove(temp_path)
            temp_path = output_path + '.temp2.gif'
            best_frames[0].save(
                temp_path,
                save_all=True,
                append_images=best_frames[1:],
                duration=best_durations,
                loop=0,
                optimize=True,
                quality=70
            )
            current_size = os.path.getsize(temp_path) / (1024 * 1024)
            print(f"Quality reduction: {current_size:.2f} MB")

        # If still too large, reduce resolution further
        if current_size > max_size_mb:
            os.remove(temp_path)
            new_size = (int(original_size[0] * 0.5), int(original_size[1] * 0.5))
            print(f"Further resizing to {new_size}")
            best_frames = []
            for frame in frames:
                best_frames.append(frame.resize(new_size, Image.Resampling.LANCZOS))

            temp_path = output_path + '.temp3.gif'
            best_frames[0].save(
                temp_path,
                save_all=True,
                append_images=best_frames[1:],
                duration=best_durations,
                loop=0,
                optimize=True,
                quality=70
            )
            current_size = os.path.getsize(temp_path) / (1024 * 1024)
            print(f"Resolution reduction: {current_size:.2f} MB")

        # If still too large, reduce frame count
        if current_size > max_size_mb and len(frames) > 60:
            os.remove(temp_path)
            target_frames = 60
            step = len(frames) // target_frames
            best_frames = frames[::step][:target_frames]
            best_durations = durations[::step][:target_frames]
            new_size = (int(original_size[0] * 0.5), int(original_size[1] * 0.5))
            best_frames = [frame.resize(new_size, Image.Resampling.LANCZOS) for frame in best_frames]

            temp_path = output_path + '.temp4.gif'
            best_frames[0].save(
                temp_path,
                save_all=True,
                append_images=best_frames[1:],
                duration=best_durations,
                loop=0,
                optimize=True,
                quality=70
            )
            current_size = os.path.getsize(temp_path) / (1024 * 1024)
            print(f"Frame reduction: {current_size:.2f} MB")

        # Move the best result to final output
        os.rename(temp_path, output_path)
        final_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Final optimized GIF: {final_size:.2f} MB")
        return final_size

if __name__ == "__main__":
    input_file = "formula_plot_animation.gif"
    output_file = "formula_plot_animation_optimized.gif"

    if os.path.exists(input_file):
        print(f"Optimizing {input_file}...")
        final_size = optimize_gif(input_file, output_file, max_size_mb=15)
        if final_size <= 15:
            print(f"SUCCESS! Optimized GIF saved as {output_file} ({final_size:.2f} MB)")
        else:
            print(f"Warning: Could not reduce below 15MB. Final size: {final_size:.2f} MB")
    else:
        print(f"Error: {input_file} not found")