/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth;

import nl.uu.cs.treewidth.algorithm.Exact;
import nl.uu.cs.treewidth.algorithm.GreedyFillIn;
import nl.uu.cs.treewidth.algorithm.TreewidthDP;
import nl.uu.cs.treewidth.algorithm.UpperBound;
import nl.uu.cs.treewidth.input.DgfReader;
import nl.uu.cs.treewidth.input.GraphInput;
import nl.uu.cs.treewidth.input.InputException;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.timing.Stopwatch;

public class Runny {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		//GraphInput gen = new RandomGraphGenerator(200,0.25);
		//CliqueGraphGenerator gen = new CliqueGraphGenerator(20);
		NGraph<InputData> g = null;
		GraphInput in = new DgfReader( "graphs/queen6_6.dgf" );
		
		try {
			g = in.get();
		} catch (InputException e) {
			// This is just a demo program; just die.
			System.out.println( "Error opening file; dumping guts." );
			e.printStackTrace();
			return;
		}

		//Output.present(g,"Voor");
		/*
		Stopwatch sw = new Stopwatch(new JavaNanoTime());

		Permutation<InputData> ub = new GreedyFillIn<InputData>();
		ub.setInput(g);
		ub.run();
		//System.out.println("Found upperbound: "+ub.getUpperBound());

		LowerBound<InputData> lb = new AllStartMaximumMinimumDegreePlusLeastC<InputData>() ;
		int runs = 0;
		sw.start();
		//while (sw.getTime() < 1000){
			lb.setInput(g);
			lb.run();
			++runs;
		//}
		sw.stop();
		System.out.println(lb.getName()+" runs "+runs+" times and used "+sw.getTime()+" milliseconds of my time and returned "+lb.getLowerBound()+".");
		*/
		/*
		try {
			g = gen.get();
		} catch (InputException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}*/
		
		/*
		
		
		GraphInput in = new DgfReader( "graphs/queen7_7.dgf" );
		
		
		try {
			g = in.get();
		} catch (InputException e) {
			// This is just a demo program; just die.
			System.out.println( "Error opening file; dumping guts." );
			e.printStackTrace();
			return;
		}
		
		CliqueGraphGenerator gen = new CliqueGraphGenerator(100);
		try {
			g = gen.get();
		} catch (InputException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println( "The graph comments:");
		System.out.println( g.getComments() );
		System.out.println( "\nEnd of graph comments.");
		*/
		/*
		System.out.println("Number of vertices before pre-processing: " + g.getNumberOfVertices());
		System.out.println("Number of edges before pre-processing: " + g.getNumberOfEdges());
		
		PreProcessor<InputData> pp = new PreProcessor<InputData>();
		pp.setInput(g);
		pp.run();
		
		System.out.println("Number of vertices after pre-processing: " + g.getNumberOfVertices());
		System.out.println("Number of edges after pre-processing: " + g.getNumberOfEdges());
		//Output.present(g,"Na");
		
		
		GreedyFillIn<InputData> ubalg = new GreedyFillIn<InputData>();
		ubalg.setInput(g);
		ubalg.run();
		System.out.println("GreedyFillIn computed an upperbound of "+ubalg.getUpperBound());
		*/
		
		UpperBound<InputData> test = new GreedyFillIn<InputData>();
		//TreewidthDP3 test = new TreewidthDP3();
		test.setInput(g);
		test.run();
		Stopwatch sw = new Stopwatch();
		Exact<InputData> alg = new TreewidthDP<InputData>(test.getUpperBound());
		alg.setInput(g);
		sw.start();
		alg.run();
		sw.stop();
		System.out.println(test.getName()+" found treewidth: "+test.getUpperBound()+" in time "+sw.getTime());
		System.out.println( "done!");
	}

}
