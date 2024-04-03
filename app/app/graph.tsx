import * as d3 from 'd3';
import {useRef, useEffect} from 'react';

export default function Graph() {
    const svgRef = useRef();

    

    useEffect(() => {
        const svg = d3.select(svgRef.current);

        svg.append('circle')
            .attr('cx', 100)
            .attr('cy', 100)
            .attr('r', 50)
            .style('fill', 'red');
    });

    return (
        <svg ref={svgRef} width={200} height={200}>
        </svg>
    );
}