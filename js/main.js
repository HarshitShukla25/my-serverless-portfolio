import React from 'react';
import ReactDOM from 'react-dom';
import ExampleWork from './example-work';


const myWork = [
    {
        'title': "Work Example",
        'href': "https://example.com",
        'desc': "lorem ipsum dolor sit amet",
        'image': {
            'desc': "example screenshot of a project involving code",
            'src': "images/example1.png",
            'comment': ""
        }
    },
    {
        'title': "Work Example",
        'href': "https://example.com",
        'desc': "lorem ipsum dolor sit amet",
        'image': {
            'desc': "example screenshot of a project involving chemistry",
            'src': "images/example2.png",
            'comment': ""
        }
    },
    {
        'title': "Work Example",
        'href': "https://example.com",
        'desc': "lorem ipsum dolor sit amet",
        'image': {
            'desc': "example screenshot of a project involving cats",
            'src': "images/example3.png",
            'comment': ""
        }
    }
]

ReactDOM.render(<ExampleWork work={myWork}/>, document.getElementById('example-work'));