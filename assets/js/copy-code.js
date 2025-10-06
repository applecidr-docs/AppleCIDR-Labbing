document.addEventListener("DOMContentLoaded", function() {
  // Select all pre > code blocks
  document.querySelectorAll('pre > code').forEach((codeBlock) => {
    // Create the button element
    const button = document.createElement('button');
    button.innerText = 'Copy';
    button.className = 'copy-button';

    // Add button before the code block
    const pre = codeBlock.parentNode;
    pre.style.position = 'relative';
    pre.insertBefore(button, codeBlock);

    // Add click event
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(codeBlock.innerText);
        button.innerText = 'Copied!';
        setTimeout(() => button.innerText = 'Copy', 2000);
      } catch (err) {
        console.error('Failed to copy: ', err);
      }
    });
  });
});
