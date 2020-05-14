import React from 'react';
import { shallow } from 'enzyme';
import ExampleWork, { ExampleWorkBubble } from '../js/example-work';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
Enzyme.configure({adapter: new Adapter()});


const myWork = [
  {
    'title': "Work Example",
    'image': {
      'desc': "example screenshot of a project involving code",
      'src': "images/example1.png",
      'comment': ""
    }
  },
  {
    'title': "Work Example",
    'image': {
      'desc': "example screenshot of a project involving cats",
      'src': "images/example3.png",
      'comment': `"Bengal cat” by roberto shabs is licensed under CC BY 2.0
                   https://www.flickr.com/photos/37287295@N00/2540855181"`
    }
  }
];
describe("ExampleWork component", () => {
let component = shallow(<ExampleWork work={myWork}/>)

  it("Should be a 'section' element", () => {
    expect(component.type()).toEqual('span');
  });

  it("Should contain as many children as their are work examples", ()=>{
    expect(component.find("ExampleWorkBubble").length).toEqual(myWork.length);
  });

  it("Should allow modal to open and close", ()=>{
    component.instance().openModal();
    expect(component.instance().state.modalOpen).toBe(true);
    component.instance().closeModal();
    expect(component.instance().state.modalOpen).toBe(false);
  });
});

describe("ExampleWorkBubble component", ()=>{
  let mockOpenModalFn = jest.fn();

  let component = shallow(<ExampleWorkBubble example={myWork[1]}
    openModal={mockOpenModalFn}/>);

  let images = component.find("img");

  it("Should contain a single 'img' element", ()=>{
    expect(images.length).toEqual(1);
  })

  it("Should have image source set correctly", ()=>{
    expect(images.prop('src')).toEqual(myWork[1].image.src);
  })

  it("Should call the open modal handler on click", ()=>{
    component.find(".section__exampleWrapper").simulate('click');

    expect(mockOpenModalFn).toHaveBeenCalled();
  })
})
