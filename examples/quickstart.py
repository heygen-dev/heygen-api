        """Minimal HeyGen example: create one prediction and print the output URL(s)."""
        import heygen_api

        output = heygen_api.run({
    "image_url": "https://example.com/input.png"
})
        print(output)
