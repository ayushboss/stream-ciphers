import java.util.LinkedList;

public class ForwardCollatz3 { // forward collatz using my own implementation of a deque using circular arrays

	public static LinkedList<Integer> generateCollatz(int n, int k) { // input: number of iterations to generate numbers
																		// for, starting number
		int iteration = n; // output: list of said generated numbers using collatz
		LinkedList2<Integer> q = new LinkedList2<Integer>();
		q.addFirst(k);
		LinkedList<Integer> list = new LinkedList<Integer>();
		for (int i = 0; i < iteration; i++) { // applies backwards collatz to first number in queue
			Integer x = q.getFirst();
			q.removeFirst();
			list.add(x);
			if (x % 3 == 1 && x > 1 && (x - 1) / 3 % 2 != 0) { // even numbers will never do 3n+1 so we eliminate those
				q.addLast((x - 1) / 3);
			}  
			q.addLast(x * 2);
		}
		return list;
	}

	public static LinkedList<Integer> mod2(LinkedList<Integer> list) { // input: any linkedlist output: linkedlist mod2
		LinkedList<Integer> bits = new LinkedList<Integer>();
		for (int i = 0; i < list.size(); i++) {
			bits.add((int) (list.get(i) % 2));
		}
		return bits;
	}

	public static LinkedList<Integer> distanceBetween(LinkedList<Integer> list) { // input: any linkedlist w/ more evens than odds
		LinkedList<Integer> distance = new LinkedList<Integer>(); // calculates the distance between any
		int count = 0;
		for (int i = 0; i < list.size(); i++) {
			if (list.get(i) %2 == 0) {
				count++;
			} else {
				distance.add(count);
				count = 0;
			}
		}
		return distance;
	}
	
	public static LinkedList<Integer> removeEvens (LinkedList<Integer> list, int k){  // input: any linkedlist with lots of evens
		LinkedList<Integer> temp = distanceBetween(list);
		int cluster = 0;  // cluster of temp we are on right now
		for(int i = 0; i<list.size(); i++) {
			if(list.get(i)%2==1) {
				
				int count = k; // number of evens to remove
				for(int j = 0; j<temp.get(cluster); j++) {  
					if((i+j+1)<list.size() && list.get(j+i+1)%2==0 && count>0) {  // removes numbers if even
						list.remove(j+i+1);
						j--;
						count--; 
					}
					else {
						break; // if we run out of even numbers continue onto next set
					}
				}
				cluster++;
			}
		}
		
		return list; 
	}
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		//System.out.println(distanceBetween(mod2(generateCollatz(10000,8))));
		//System.out.println(distanceBetween(mod2(removeEvens(generateCollatz(10000,8),1))));
		
		LinkedList<Integer> A = generateCollatz(10000,8);
		
		System.out.println(distanceBetween(A));
		System.out.println(distanceBetween(removeEvens(A,1)));
		
		/*
		int itr = 10000; // the number of collatz numbers to be generated
		int start = 8; // number to start collatz generation
		for (int i = 0; i < 100; i++) {
			int x = (i + 1) * 100;
			LinkedList<Integer> list = mod2(distanceBetween(mod2(removeEvens(generateCollatz(x, start),2))));
			int ones = 0;
			int zeroes = 0;
			for (int j = 0; j < list.size(); j++) {
				if (list.get(j) == 1)
					ones++;
				else
					zeroes++;
			}
			int diff = ones - zeroes;
			int total = ones+zeroes; 

			System.out.println("itr: " + x + " ones: " + ones + " zeroes: " + zeroes + " diff: " + diff + " ratio: "
					+ (diff / (double) total));
		}
		*/

	}

}

