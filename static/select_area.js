const gemstoneImg = document.getElementById('gemstoneImg');
        const colorPickerCanvas = document.getElementById('colorPickerCanvas');
        const selectionBox = document.getElementById('selectionBox');
        const colorDisplay = document.getElementById('colorDisplay');
        const cssColorCodeElement = document.getElementById('cssColorCode');
        const rgbValuesElement = document.getElementById('rgbValues');
        const brightnessElement = document.getElementById('brightness');
        const colorRatiosElement = document.getElementById('colorRatios');
        const densityElement = document.getElementById('density');
        const colorResultsElement = document.getElementById('colorResults');
        const detectColorButton = document.getElementById('detectColor');
        const saveButton = document.getElementById('saveColorData');

        let isDrawing = false;
        let startX, startY, endX, endY;

        gemstoneImg.onload = function () {
            colorPickerCanvas.width = gemstoneImg.width;
            colorPickerCanvas.height = gemstoneImg.height;
            const ctx = colorPickerCanvas.getContext('2d');
            ctx.drawImage(gemstoneImg, 0, 0, gemstoneImg.width, gemstoneImg.height);
        };

        colorPickerCanvas.addEventListener('mousedown', function (event) {
            isDrawing = true;
            const rect = colorPickerCanvas.getBoundingClientRect();
            startX = event.clientX - rect.left;
            startY = event.clientY - rect.top;
            selectionBox.style.left = `${startX}px`;
            selectionBox.style.top = `${startY}px`;
            selectionBox.style.width = '0px';
            selectionBox.style.height = '0px';
            selectionBox.style.display = 'block';
        });

        colorPickerCanvas.addEventListener('mousemove', function (event) {
            if (isDrawing) {
                const rect = colorPickerCanvas.getBoundingClientRect();
                endX = event.clientX - rect.left;
                endY = event.clientY - rect.top;
                const width = endX - startX;
                const height = endY - startY;
                selectionBox.style.width = `${Math.abs(width)}px`;
                selectionBox.style.height = `${Math.abs(height)}px`;
                if (width < 0) selectionBox.style.left = `${endX}px`;
                if (height < 0) selectionBox.style.top = `${endY}px`;
            }
        });

        colorPickerCanvas.addEventListener('mouseup', function () {
            isDrawing = false;

            const ctx = colorPickerCanvas.getContext('2d');
            const imageData = ctx.getImageData(startX, startY, Math.abs(endX - startX), Math.abs(endY - startY));
            const data = imageData.data;

            let r = 0, g = 0, b = 0, count = 0;
            for (let i = 0; i < data.length; i += 4) {
                r += data[i];
                g += data[i + 1];
                b += data[i + 2];
                count++;
            }

            r = Math.round(r / count);
            g = Math.round(g / count);
            b = Math.round(b / count);

            const colorCode = `rgb(${r}, ${g}, ${b})`;
            colorDisplay.style.backgroundColor = colorCode;
            cssColorCodeElement.textContent = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
            rgbValuesElement.textContent = `(${r}, ${g}, ${b})`;
            brightnessElement.textContent = Math.round((r + g + b) / 3);
            colorRatiosElement.textContent = `R: ${(r / (r + g + b)).toFixed(2)}, G: ${(g / (r + g + b)).toFixed(2)}, B: ${(b / (r + g + b)).toFixed(2)}`;
            densityElement.textContent = (data.length / (colorPickerCanvas.width * colorPickerCanvas.height)).toFixed(2);
        });

        detectColorButton.addEventListener('click', function () {
        const r = parseInt(rgbValuesElement.textContent.match(/\d+/g)[0]);
        const g = parseInt(rgbValuesElement.textContent.match(/\d+/g)[1]);
        const b = parseInt(rgbValuesElement.textContent.match(/\d+/g)[2]);

        console.log("Sending RGB values:", r, g, b);  // ✅ Debugging: Log sent values

        fetch('/color/closest_color/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ color: [r, g, b] })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server Response:", data);  // ✅ Debugging: Log server response

            colorResultsElement.innerHTML = "";  // Clear previous results
            if (data.colors) {
                data.colors.forEach(color => {
                    let li = document.createElement('li');
                    li.textContent = `${color.name} - ${color.percentage}%`;
                    colorResultsElement.appendChild(li);
                });
            } else {
                colorResultsElement.innerHTML = "<li>No gemstone color found.</li>";
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
});


saveButton.addEventListener('click', function () {
    console.log("🟢 Save Color Data Button Clicked"); // ✅ Debugging

    const r = parseInt(rgbValuesElement.textContent.match(/\d+/g)[0]);
    const g = parseInt(rgbValuesElement.textContent.match(/\d+/g)[1]);
    const b = parseInt(rgbValuesElement.textContent.match(/\d+/g)[2]);

    const colorData = {
        image_id: "{{ gemstone.id }}",
        rgb: [r, g, b],
        css_color_code: cssColorCodeElement.textContent,
        brightness: parseFloat(brightnessElement.textContent),
        color_ratios: colorRatiosElement.textContent,
        density: parseFloat(densityElement.textContent)
    };

    console.log("📤 Sending Color Data:", colorData);  // ✅ Debugging

    fetch('/save_color/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(colorData)
    })
    .then(response => {
        console.log("🔵 Server Response Received"); // ✅ Debugging
        return response.json();
    })
    .then(data => {
        console.log("🟣 Server Response Data:", data);  // ✅ Debugging
        if (data.message) {
            alert(data.message);
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("❌ Fetch Error:", error);
    });
});