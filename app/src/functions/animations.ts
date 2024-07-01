import {createAnimation} from "@ionic/vue";

export const defaultRemedeMainToolbarAnimation = (element: Element | Element[] | Node | Node[] | NodeList) => createAnimation()
    .addElement(element)
    .duration(250)
    .fromTo("transform", "translateY(0)", "translateY(-100%)")
    .fromTo("opacity", "1", "0")

export const defaultRemedeSearchToolbarAnimation = (element: Element | Element[] | Node | Node[] | NodeList) => createAnimation()
    .addElement(element)
    .beforeAddClass('mt')
    .duration(250)
    .fromTo("transform", "translateY(0)", "translateY(-50%)")
    .fromTo("scale", "1", "1.01")

export const defaultRemedeContentAnimation = (element: Element | Element[] | Node | Node[] | NodeList) => createAnimation()
    .addElement(element)
    .duration(250)
    .fromTo("transform", "translateY(0)", "translateY(-10%)")
