const DrawingMode = {
    Node: 0,
    Edge: 1,
    Erase: 2
}

class DrawingEditor {
    canvas; 
    drawingMode;
    drawerOptions;
    isDown;
    color;
    groundY;
    groundLine;
    selectedNode;
    radius = 10;


    constructor(selector, canvasHeight, canvasWidth) {
        $(`#${selector}`)
            .replaceWith(`<canvas id="${selector}" height=${canvasHeight} width=${canvasWidth}> </canvas>`);
        
        this.canvas = new fabric.Canvas(`${selector}`, { selection: false });
        this.color = $('input[name=options]:checked', '#controls').val();
        this.drawingMode = DrawingMode.Draw;
        this.isDown = false;
        this.initializeCanvasEvents();
        this.groundY = this.canvas.getHeight() - 0.2*(this.canvas.getHeight());
        this.groundLine = new fabric.Line([0, this.groundY, this.canvas.getWidth(), this.groundY], {
            stroke: 'black',
            strokeWidth: 2,
            selectable: false,
            hasBorders: false
        })
        this.canvas.add(this.groundLine);
        this.selectedNode = null;
    }

    initializeCanvasEvents() {
        this.canvas.on('mouse:down', (o) => {
            if (this.drawingMode == DrawingMode.Node) {
                const pointer = this.canvas.getPointer(o.e);
                let yCoord = pointer.y - 10

                if (yCoord >= this.groundY - 30) {
                    yCoord = this.groundY - 10
                }

                let circle = new fabric.Circle({
                    fill: 'white',
                    stroke: 'black',
                    strokeWidth: 2,
                    left: pointer.x - this.radius,
                    top: yCoord,
                    radius: this.radius,
                    selectable: false
                })
                this.canvas.add(circle);
                console.log(pointer.x, pointer.y);
            }
            else if (this.drawingMode == DrawingMode.Edge) {
                if (o.target != null) {
                    if (o.target.get('type') == 'circle') {
                        if (this.selectedNode == null) {
                            this.selectedNode = o.target;
                            o.target.stroke = this.color;
                            o.target.dirty = true;
                            this.canvas.renderAll();
                        }
                        else {
                            let points = [
                                this.selectedNode.left + this.selectedNode.radius,
                                this.selectedNode.top + this.selectedNode.radius,
                                o.target.left + o.target.radius,
                                o.target.top + o.target.radius
                            ]

                            let line = new fabric.Line(points, {
                                stroke: this.color,
                                strokeWidth: 3,
                                selectable: false
                            });
                            this.canvas.add(line);
                            line.moveTo(0)

                            this.selectedNode.stroke = 'black';
                            this.selectedNode.dirty = true;
                            this.canvas.renderAll();
                            this.selectedNode = null;
                        }
                    }
                }
                else {
                    if (this.selectedNode != null) {
                        this.selectedNode.stroke = 'black';
                        this.selectedNode.dirty = true;
                        this.canvas.renderAll();
                        this.selectedNode = null;
                    }
                    this.selectedNode = null;
                }
            }
            else if (this.drawingMode == DrawingMode.Erase) {
                if (o.target) {
                    if (o.target != this.groundLine) {
                        this.canvas.remove(o.target);
                    }
                }
            }
        });
    }
}
  