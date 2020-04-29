let webSettings = async () => {
    let grepConf = () => {
        return fetch('../../config.json').then((data) => {
            return data.json();
        })
    }

    let setConfig = (target, config) => {
        let keys = Object.keys(target);

        keys.forEach((key) => {
            if (key == 'githubLink') {
                target['author'].href = config[key];
            } else if (key == 'backgroundColor') {
                target[key].style.background = config[key];
            } else if (key == 'postedOnText') {
                [...target[key]].map((span) => span.innerHTML = config[key])
            } else {
                target[key].innerHTML = config[key];
            }

        });

    }


    let {
        title,
        description,
        author,
        backgroundColor,
        year,
        postedOnText,
        githubLink
    } = await grepConf();


    let target = {
        title: document.querySelector('#title'),
        description: document.querySelector('#description'),
        author: document.querySelector('#author'),
        backgroundColor: document.querySelector('body'),
        year: document.querySelector('#year'),
        postedOnText: document.querySelectorAll('.postedOnText'),
        githubLink: 0
    }

    let yearNow = new Date().getFullYear();

    let conf = {
        title: title || "My Note Page",
        description: description || "* Sharing is Caring *",
        author: author || "Defri Indra Mahardika",
        backgroundColor: backgroundColor || "linear-gradient(0deg, #eccb70,#be7d57)",
        year: year || yearNow,
        postedOnText: postedOnText || "Posted On:",
        githubLink: githubLink || "#"
    }

    setConfig(target, conf);

}

let confNoted = async () => {
    let conf = {
        target: document.querySelector('#posts'),
        template: (post, date) => {
            let div = document.createElement('div');
            div.setAttribute('class', 'post');

            let pLabel = document.createElement('p');
            pLabel.setAttribute('class', 'postedon__label');

            let spanDateLabel = document.createElement('span');
            spanDateLabel.setAttribute('class', 'postedOnText');

            let spanDateContent = document.createElement('span');
            spanDateContent.setAttribute('class', 'post_date');
            spanDateContent.innerHTML = ` ${date}`;

            pLabel.appendChild(spanDateLabel);
            pLabel.appendChild(spanDateContent);

            let pContent = document.createElement('p');
            pContent.innerHTML = `${post.replace('\n','<br>')}`;

            div.appendChild(pLabel);
            div.appendChild(pContent);

            return div;
        }
    }

    let grepNote = async () => {
        return fetch('../noted/source.json').then((data) => {
            return data.json();
        });
    }

    let propSort = (array, prop, desc) => {
        array.sort( (a, b) => {
            if (a[prop] < b[prop])
                return desc ? 1 : -1;
            if (a[prop] > b[prop])
                return desc ? -1 : 1;
            return 0;
        });
    }

    files = await grepNote();

    propSort(files,'date',true);

    files.filter((file) => {
        conf.target.appendChild(
            conf.template(file.post, file.date)
        );
    })

}

confNoted().then(() => {
    webSettings();
});
