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
 
package nl.uu.cs.treewidth.testing;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.ArrayList;
import java.util.TreeMap;

import nl.uu.cs.treewidth.algorithm.Algorithm;
import nl.uu.cs.treewidth.algorithm.AllStartLexBFS;
import nl.uu.cs.treewidth.algorithm.AllStartMaximumCardinalitySearch;
import nl.uu.cs.treewidth.algorithm.AllStartMaximumCardinalitySearchMinimal;
import nl.uu.cs.treewidth.algorithm.AllStartMaximumMinimumDegree;
import nl.uu.cs.treewidth.algorithm.AllStartMaximumMinimumDegreePlusLeastC;
import nl.uu.cs.treewidth.algorithm.AllStartMinorMinWidth;
import nl.uu.cs.treewidth.algorithm.Exact;
import nl.uu.cs.treewidth.algorithm.GreedyDegree;
import nl.uu.cs.treewidth.algorithm.GreedyFillIn;
import nl.uu.cs.treewidth.algorithm.LexBFS;
import nl.uu.cs.treewidth.algorithm.LowerBound;
import nl.uu.cs.treewidth.algorithm.MaximumCardinalitySearch;
import nl.uu.cs.treewidth.algorithm.MaximumCardinalitySearchMinimal;
import nl.uu.cs.treewidth.algorithm.MaximumMinimumDegree;
import nl.uu.cs.treewidth.algorithm.MaximumMinimumDegreePlusLeastC;
import nl.uu.cs.treewidth.algorithm.MaximumMinimumDegreePlusMaxD;
import nl.uu.cs.treewidth.algorithm.MaximumMinimumDegreePlusMinD;
import nl.uu.cs.treewidth.algorithm.MinDegree;
import nl.uu.cs.treewidth.algorithm.MinorMinWidth;
import nl.uu.cs.treewidth.algorithm.PermutationToTreeDecomposition;
import nl.uu.cs.treewidth.algorithm.Ramachandramurthi;
import nl.uu.cs.treewidth.algorithm.TreewidthDP;
import nl.uu.cs.treewidth.algorithm.UpperBound;
import nl.uu.cs.treewidth.input.DgfReader;
import nl.uu.cs.treewidth.input.GraphInput;
import nl.uu.cs.treewidth.input.InputException;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.output.Output;

public class ResultChecker {
	
	public static interface AlgoCreator<D extends InputData> {
		Algorithm<D> create();
	}

	public static TestType testType( String t ) {
		if( t.equals("lowerbound") )
			return TestType.LOWERBOUND;
		else if( t.equals("upperbound") )
			return TestType.UPPERBOUND;
		else 
			return TestType.EXACT;
	}
	public static enum TestType {
		LOWERBOUND,
		UPPERBOUND,
		EXACT
	}
	
	public static class Test {
		Test( TestType type, AlgoCreator<InputData> c, String file, int answer, String ref ) {
			this.type = type;
			algoCreator = c;
			graphFile = file;
			this.answer = answer;
			reference = ref==null? "by hand" : ref;
		}
		TestType type;
		AlgoCreator<InputData> algoCreator;
		String graphFile;
		int answer;
		String reference;
		boolean check() {
			System.out.print(".");
			Algorithm<InputData> a = algoCreator.create();
			NGraph<InputData> g = null;
			GraphInput input = new DgfReader( graphFile );
			try {
				g = input.get();
			} catch (InputException e) {
				Output.bugreport( "ResultChecker says: DgfReader failed on '"+graphFile+"' while testing whether "+a.getName()+" would give "+answer );
				return false;
			}
			a.setInput( g );
			a.run();
			int result = -1;
			switch( type ) {
			case LOWERBOUND:
				if( a instanceof LowerBound ) {
					result = ((LowerBound<InputData>)a).getLowerBound();
				} else {
					System.err.println( "ResultChecker says: "+a.getName()+" is not a lowerbound." );
					return false;
				}
				break;
			case UPPERBOUND:
				if( a instanceof UpperBound ) {
					result = ((UpperBound<InputData>)a).getUpperBound();
				} else {
					System.err.println( "ResultChecker says: "+a.getName()+" is not an upperbound." );
					return false;
				}
				break;
			case EXACT:
				if( a instanceof Exact ) {
					result = ((Exact<InputData>)a).getTreewidth();
				} else {
					System.err.println( "ResultChecker says: "+a.getName()+" is not an exact." );
					return false;
				}
				break;
			default:
				System.err.println( "ResultChecker says: there seems to be an algorithm that is none of LowerBound, UpperBound or Exact; it is called " + a.getName() );
				return false;
			}
			if( result != answer ) {
				Output.bugreport( "ResultChecker says: "+a.getName()+" gives a "+type+" of "+result+" on graph '"+graphFile+"', but according to this testcase it should be "+answer+". (Source of this answer: "+reference+")" );
			}
			return true;
		}
	}
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		System.out.println( "Regression testing ftw." );
		System.out.println();
		
		TreeMap< String, AlgoCreator<InputData> > creators = new TreeMap<String,AlgoCreator<InputData>>();
		creators.putAll( makeLBCreators() );
		creators.putAll( makeUBCreators() );
		creators.putAll( makeExactCreators() );
		//System.out.println(creators);
		
		ArrayList<Test> tests = new ArrayList<Test>();
		
		String testFile = "default.tests";
		
		FileReader fr;
		LineNumberReader in = null;
		try {
			fr = new FileReader(testFile);
		} catch (FileNotFoundException e) {
			System.err.println( "Error opening file '"+testFile+"'." );
			return;
		}
		in = new LineNumberReader( fr );

		System.out.println( "Parsing test descriptions." );
		String line;
		try {
			// read the entire file line by line.
			while( (line=in.readLine()) !=null ) {
				
				if (line.charAt(0)=='#') continue;
				
				System.out.print(".");
				
				// tokenize the line
				String[] tokens = line.split("\\t");
				assert tokens.length > 0;
				
				if( tokens.length==5 ) {
					
					String type = tokens[0];
					String algo = tokens[1];
					String graph = tokens[2];
					String answer = tokens[3];
					String ref = tokens[4];
					
					AlgoCreator<InputData> ac = creators.get(algo);
					if( ac==null )
						System.out.println( "'"+algo+"' is not a valid algorithm. (Line "+in.getLineNumber()+")" );
					else
						tests.add( new Test(
								testType(type),
								ac,
								graph,
								Integer.parseInt(answer),
								ref
								));
						
				} else {
					//System.out.println( "Wrong number of tokens on line "+in.getLineNumber() );
				}
				
			}
		} catch (IOException e) {}
		
		System.out.println( "\nRunning tests." );
		for( Test t : tests ) {
			t.check();
		}
		
		System.out.println();
		System.out.println();
		System.out.println("Done.");

	}
	private static TreeMap<String, AlgoCreator<InputData>> makeLBCreators() {
		TreeMap<String,AlgoCreator<InputData>> map = new TreeMap< String, AlgoCreator<InputData> >();
		map.put("AllStartMaximumMinimumDegree",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new AllStartMaximumMinimumDegree<InputData>();
				} }
			);
		map.put("AllStartMaximumMinimumDegreePlusLeastC",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new AllStartMaximumMinimumDegreePlusLeastC<InputData>();
				} }
			);
		map.put("AllStartMinorMinWidth",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new AllStartMinorMinWidth<InputData>();
				} }
			);
		map.put("MaximumCardinalitySearch",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MaximumCardinalitySearch<InputData>();
				} }
			);
		map.put("MaximumMinimumDegree",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MaximumMinimumDegree<InputData>();
				} }
			);
		map.put("MaximumMinimumDegreePlusLeastC",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MaximumMinimumDegreePlusLeastC<InputData>();
				} }
			);
		map.put("MaximumMinimumDegreePlusMaxD",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MaximumMinimumDegreePlusMaxD<InputData>();
				} }
			);
		map.put("MaximumMinimumDegreePlusMinD",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MaximumMinimumDegreePlusMinD<InputData>();
				} }
			);
		map.put("MinDegree",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MinDegree<InputData>();
				} }
			);
		map.put("MinorMinWidth",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new MinorMinWidth<InputData>();
				} }
			);
		map.put("Ramachandramurthi",
				new AlgoCreator<InputData>() { public LowerBound<InputData> create() {
					return new Ramachandramurthi<InputData>();
				} }
			);
		return map;
	}
	
	private static TreeMap<String, AlgoCreator<InputData>> makeUBCreators() {
		TreeMap<String,AlgoCreator<InputData>> map = new TreeMap< String, AlgoCreator<InputData> >();
		map.put("AllStartLexBFS",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new AllStartLexBFS<InputData>();
				} }
			);
		map.put("GreedyDegree",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new GreedyDegree<InputData>();
				} }
			);
		map.put("GreedyFillIn",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new GreedyFillIn<InputData>();
				} }
			);
		map.put("AllStartLexBFS",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new PermutationToTreeDecomposition<InputData>( new AllStartLexBFS<InputData>() );
				} }
			);
		map.put("AllStartMaximumCardinalitySearch",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new PermutationToTreeDecomposition<InputData>( new AllStartMaximumCardinalitySearch<InputData>() );
				} }
			);
		map.put("AllStartMaximumCardinalitySearchMinimal",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new PermutationToTreeDecomposition<InputData>( new AllStartMaximumCardinalitySearchMinimal<InputData>() );
				} }
			);
		map.put("LexBFS",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new PermutationToTreeDecomposition<InputData>( new LexBFS<InputData>() );
				} }
			);
		map.put("MaximumCardinalitySearch",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new PermutationToTreeDecomposition<InputData>( new MaximumCardinalitySearch<InputData>() );
				} }
			);
		map.put("MaximumCardinalitySearchMinimal",
				new AlgoCreator<InputData>() { public UpperBound<InputData> create() {
					return new PermutationToTreeDecomposition<InputData>( new MaximumCardinalitySearchMinimal<InputData>() );
				} }
			);

		return map;
	}
	
	private static TreeMap<String, AlgoCreator<InputData>> makeExactCreators() {
		TreeMap<String,AlgoCreator<InputData>> map = new TreeMap< String, AlgoCreator<InputData> >();
		map.put("TreewidthDP+GreedyDegree",
				new AlgoCreator<InputData>() { public Exact<InputData> create() {
					return new TreewidthDP<InputData>(new GreedyDegree<InputData>());
				} }
			);
		map.put("TreewidthDP+GreedyFillIn",
				new AlgoCreator<InputData>() { public Exact<InputData> create() {
					return new TreewidthDP<InputData>(new GreedyFillIn<InputData>());
				} }
			);
		return map;
	}

}
